# AINS6003 Deep Learning & Neural Networks

Jupyter Book course repository for **AINS6003** / Aurnova **AIN6003** — Deep Learning & Neural Networks.

[Open in GitHub Codespaces](https://codespaces.new/CastaliaInstitute/ains-6003-deep-learning-and-neural-networks)

Structure follows [CastaliaInstitute/ains-6001-foundations-of-artificial-intelligence](https://github.com/CastaliaInstitute/ains-6001-foundations-of-artificial-intelligence) and the Jupyter Book / MyST pattern used in [CastaliaInstitute/aima](https://github.com/CastaliaInstitute/aima).

## Contents

- prose chapters per module
- Thebe-enabled assignment notebooks
- RISE-ready slide notebooks
- slide narration and instructor notes
- executable lab notebooks (Modules 1–8)

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make html
```

## Codespaces

Open the repository in GitHub Codespaces to get a preconfigured Python/Jupyter environment. The Codespace installs `requirements.txt`, registers a `Python 3 (AINS6003)` kernel, and forwards ports for JupyterLab and local Jupyter Book previews.

Launch link: https://codespaces.new/CastaliaInstitute/ains-6003-deep-learning-and-neural-networks

Useful commands inside the Codespace:

```bash
make html
python -m http.server 8000 --directory _build/html
jupyter lab --ip 0.0.0.0 --port 8888 --no-browser
```

## Export formats

- `make html` — web book
- `make pdf` — LaTeX PDF (CI also builds on push)
- `make epub` — EPUB export

## Publishing

Push to `main` to publish via GitHub Pages (see `.github/workflows/pages.yml`).

The deployed site has:

- **Front page** — `index.html` (course hub, links to book and slides)
- **Jupyter Slides index** — `slides/index.html` (links to each module `slides.html`)
- **Jupyter Book** — `book/` (full course: prose, assignments, labs, slide pages)

Preview locally: `make site` then open `site/index.html` (use a local server if book assets need correct paths).

**Canonical URL:** https://ains6003.courses.castalia.institute/ (Cloudflare-proxied CNAME → GitHub Pages).

Fallback: https://castaliainstitute.github.io/ains-6003-deep-learning-and-neural-networks/

See [docs/CUSTOM_DOMAIN.md](docs/CUSTOM_DOMAIN.md) for DNS, TLS, and Zero Trust Access.

See [docs/AURNOVA_DEPLOYMENT.md](docs/AURNOVA_DEPLOYMENT.md) for the Aurnova cohort, Populi roster, and student assignment repository provisioning model.
