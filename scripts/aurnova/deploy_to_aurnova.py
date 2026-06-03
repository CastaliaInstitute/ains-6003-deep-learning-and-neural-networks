#!/usr/bin/env python3
"""Deploy the Castalia course source into an Aurnova instructor repository.

The deployment copy is intentionally sanitized:

- local build/runtime directories are excluded
- Castalia-specific Pages CNAME is removed; customer DNS is not configured
- cohort workflow defaults are pointed at the Aurnova instructor repo

By default the script runs in dry-run mode. Use --live to create/push the target
repository.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "_build",
    "site",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}


def run(args: list[str], cwd: Path, *, dry_run: bool = False) -> None:
    print("+", " ".join(args))
    if dry_run:
        return
    subprocess.run(args, cwd=cwd, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-org", default="Aurnova")
    parser.add_argument("--target-repo", default="ain6003-instructor")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--visibility", choices=["private", "public", "internal"], default="private")
    parser.add_argument("--live", action="store_true", help="Create/push the target repository")
    parser.add_argument("--force", action="store_true", help="Use --force-with-lease when pushing")
    parser.add_argument("--skip-build", action="store_true", help="Skip make site validation")
    parser.add_argument("--keep-workdir", action="store_true", help="Keep the temporary deployment directory")
    return parser.parse_args()


def should_copy(path: Path) -> bool:
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return False
    if path.suffix in EXCLUDE_SUFFIXES:
        return False
    if path.name == ".DS_Store":
        return False
    return True


def copy_source(dest: Path) -> None:
    for src in ROOT.rglob("*"):
        rel = src.relative_to(ROOT)
        if not should_copy(rel):
            continue
        target = dest / rel
        if src.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)


def replace_text(path: Path, replacements: dict[str, str]) -> None:
    if not path.exists():
        return
    text = path.read_text()
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text)


def sanitize(dest: Path, target_org: str, target_repo: str) -> None:
    cname = dest / "pages" / "CNAME"
    if cname.exists():
        cname.unlink()

    canonical = f"{target_org}/{target_repo}"
    replacements = {
        "Aurnova/ain6003-course": canonical,
        "aurnova/ain6003-course": canonical,
        "Cloudflare-proxied CNAME \u2192 GitHub Pages": "private GitHub Pages in Aurnova",
        "https://ains6003.courses.castalia.institute/": "Aurnova private Pages URL",
    }
    for path in [
        dest / "README.md",
        dest / "docs" / "AURNOVA_DEPLOYMENT.md",
        dest / ".github" / "workflows" / "create-cohort.yml",
    ]:
        replace_text(path, replacements)


def repo_exists(owner: str, repo: str) -> bool:
    result = subprocess.run(
        ["gh", "repo", "view", f"{owner}/{repo}", "--json", "name"],
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def create_or_confirm_repo(args: argparse.Namespace, dry_run: bool) -> None:
    full_name = f"{args.target_org}/{args.target_repo}"
    if repo_exists(args.target_org, args.target_repo):
        print(f"repo exists: {full_name}")
        return
    visibility_flag = f"--{args.visibility}"
    run(
        [
            "gh",
            "repo",
            "create",
            full_name,
            visibility_flag,
            "--description",
            "AINS6003 instructor-facing course repository",
            "--disable-wiki",
        ],
        ROOT,
        dry_run=dry_run,
    )


def git_commit_and_push(dest: Path, args: argparse.Namespace, dry_run: bool) -> None:
    remote = f"https://github.com/{args.target_org}/{args.target_repo}.git"
    run(["git", "init", "-b", args.branch], dest, dry_run=dry_run)
    run(["git", "config", "user.name", "aurnova-deploy"], dest, dry_run=dry_run)
    run(["git", "config", "user.email", "automation@aurnova.ai"], dest, dry_run=dry_run)
    run(["git", "add", "."], dest, dry_run=dry_run)
    run(["git", "commit", "-m", "Deploy AINS6003 instructor course"], dest, dry_run=dry_run)
    run(["git", "remote", "add", "origin", remote], dest, dry_run=dry_run)
    push = ["git", "push", "origin", args.branch]
    if args.force:
        push.append("--force-with-lease")
    run(push, dest, dry_run=dry_run)


def main() -> None:
    args = parse_args()
    dry_run = not args.live

    if not args.skip_build:
        run(["make", "site"], ROOT, dry_run=False)

    workdir = Path(tempfile.mkdtemp(prefix="ain6003-aurnova-deploy-"))
    try:
        print(f"deployment workdir: {workdir}")
        copy_source(workdir)
        sanitize(workdir, args.target_org, args.target_repo)
        create_or_confirm_repo(args, dry_run=dry_run)
        git_commit_and_push(workdir, args, dry_run=dry_run)
    finally:
        if args.keep_workdir:
            print(f"kept deployment workdir: {workdir}")
        else:
            shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
