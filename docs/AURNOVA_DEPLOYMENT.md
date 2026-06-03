# Aurnova Course Deployment Model

## Goal

Deliver AINS6003 as a canonical Aurnova course package that instructors can instantiate per cohort, connect to Populi, and use to provision private student assignment repositories.

## Required Platform Decisions

1. Aurnova should use GitHub Enterprise Cloud.
2. The canonical course repository should be private.
3. GitHub Pages for instructor/cohort control pages should be private.
4. Privileged operations should run in GitHub Actions or a backend service, not directly from static Pages JavaScript.
5. Populi is the system of record for enrollment and grades.

Private GitHub Pages access control is an Enterprise Cloud feature. Static Pages can collect input, but it cannot safely hold a token that creates repos or teams. For the first deployable version, the "form" is a `workflow_dispatch` form in GitHub Actions. A later version can replace that with an LTI 1.3 or GitHub App backend.

## Repository Topology

Canonical Aurnova repositories:

```text
Aurnova/ain6003-course
Aurnova/ain6003-assignment-m01
Aurnova/ain6003-assignment-m02
Aurnova/ain6003-assignment-m03
Aurnova/ain6003-assignment-m04
Aurnova/ain6003-assignment-m05
Aurnova/ain6003-assignment-m06
Aurnova/ain6003-assignment-m07
Aurnova/ain6003-assignment-m08
```

Cohort/instructor repositories:

```text
Aurnova/ain6003-fall2026-course
Aurnova/ain6003-fall2026-m01-template
Aurnova/ain6003-fall2026-m02-template
...
Aurnova/ain6003-fall2026-m08-template
```

Student repositories:

```text
Aurnova/ain6003-fall2026-m01-<github_username>
Aurnova/ain6003-fall2026-m02-<github_username>
...
```

## End-to-End Flow

1. Customer purchases course access at `courses.castalia.institute`.
2. Castalia/Aurnova operator provisions the customer into the Aurnova GitHub Enterprise organization.
3. Operator creates or updates the canonical deliverable repo:
   - `Aurnova/ain6003-course`
   - private repo
   - private GitHub Pages enabled
   - contains cohort creation workflow
4. Operator runs `Create Aurnova Cohort` from the canonical repo.
5. The workflow creates:
   - cohort course repo
   - cohort assignment template repos
   - instructor team
   - optional instructor GitHub memberships
6. Instructor configures the cohort course repo secrets:
   - `AURNOVA_GH_TOKEN`
   - `POPULI_API_BASE`
   - `POPULI_API_KEY`
   - optional `POPULI_COURSE_OFFERING_ID`
7. Instructor runs roster sync from the cohort repo.
8. Instructor reviews generated roster.
9. Instructor runs assignment repo provisioning.
10. Students are added directly as outside collaborators to the cohort course repo and to their own private assignment repos.
11. Students open the cohort page, copy/start the assignment, and work in their own repo/Codespace.
12. Autograding runs in each student repo.
13. Instructor collects grade artifacts and posts grades back to Populi manually, by CSV, or later through LTI/Populi API automation.

## Permission Model

Instructor team:

```text
ain6003-fall2026-instructors
```

Permissions:

- admin or maintain access to cohort course repo
- admin or maintain access to cohort assignment templates
- maintain access to generated student repositories

Students are outside collaborators, not cohort team members.

Permissions:

- direct `pull` access to the cohort course repo
- direct `push` access only to the student's own generated assignment repos
- no blanket team access to other students' assignment repos

## Naming Rules

Cohort names must be lowercase and URL-safe:

```text
fall2026
spring2027
summer2027
```

Repository names:

```text
<course>-<cohort>-course
<course>-<cohort>-mNN-template
<course>-<cohort>-mNN-<github_username>
```

Example:

```text
ain6003-fall2026-m01-jane-student
```

## Current Implementation

This repo includes:

- `.github/workflows/create-cohort.yml`
- `.github/workflows/sync-populi-roster.yml`
- `.github/workflows/create-student-assignment-repos.yml`
- `scripts/aurnova/create_cohort.py`
- `scripts/aurnova/sync_populi_roster.py`
- `scripts/aurnova/create_student_assignment_repos.py`

The scripts are designed to run in dry-run mode first. They require explicit secrets before creating or modifying GitHub resources.

## Open Items Before Production

1. Confirm Aurnova GitHub Enterprise Cloud org name.
2. Confirm that outside collaborators are enabled for the Aurnova organization.
3. Confirm Populi tenant URL and API permissions.
4. Confirm grade return path:
   - manual Populi entry
   - Populi CSV import
   - Populi API
   - LTI 1.3 Assignment and Grade Services
5. Decide whether assignment repos are one per module or one per student for the whole course.

Recommendation: use one repo per student per module for clearer deadlines, autograding, and audit history.
