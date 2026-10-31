# Proposed branch protection (human-administered)

**Status:** recommendation only. No repository rules, settings, or protections were changed by this PR.

Apply a ruleset to `main` (and any future protected release branch) with:

1. Require pull requests; prohibit direct pushes.
2. Require at least **one approving human review** from someone other than the PR author. Do not count the author or an automation identity as the independent human.
3. Require the repository's stable test/status checks by their exact check names after they have been observed on the intended workflow. Do not guess check names. Require branches to be up to date if operationally appropriate.
4. Dismiss stale approvals when new commits are pushed; require approval of the most recent reviewable push.
5. Block force pushes and branch deletion.
6. Require conversation resolution before merge.
7. Enable secret scanning and push protection where available for the repository plan.
8. Keep merge rights with human maintainers. Do not enable auto-merge for this review channel.
9. Ensure CODEOWNERS review is requested, while remembering CODEOWNERS alone does not prevent self-approval or enforce a human review.
10. Restrict who can bypass the ruleset; ideally no bypass for routine changes.

## Scope and operational notes

- Configure protections in GitHub repository settings / rulesets. This document does not apply them.
- The exact required status-check names must be selected from checks actually reported by GitHub for the intended workflow.
- GitHub plan, repository visibility, and organization policy may affect availability of secret scanning and push protection.
- Keep the review branch `chore/review-channel` separate from `main`; do not use this proposal to change protections on unrelated PRs.
- Human owner must verify settings after applying them and record a screenshot or exported ruleset evidence.
