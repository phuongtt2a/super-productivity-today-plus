# Contributing to Today+

Thanks for helping make Today+ useful and calm. This is a community plugin for Super Productivity.

1. Check existing GitHub Issues and open an issue for each bug or enhancement. Link all development work to the issue.
2. Include the Super Productivity version, operating system, whether you use mobile, and clear reproduction steps. Use **test data**; never include personal task details, tokens, or account backups.
3. Keep the interface accessible, responsive, keyboard-friendly and compatible with host light/dark themes and Vietnamese text.
4. Use supported Plugin API calls; avoid direct access to Super Productivity internals or external services.
5. Create an issue-linked branch (for example `fix/23-task-action`), commit with the issue number (for example `fix: avoid lost taps (#23)`), and open a PR with `Closes #23` when appropriate. Run the package/unit and browser integration tests before review.
6. Keep screenshots and README accurate if UI changes.

Please do not commit user data or credentials. See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).

Merging a tested pull request into `main` automatically publishes the newest installable ZIP to the matching GitHub Release. Same-version fixes refresh the release asset; a version bump creates a new release. See [release instructions](docs/RELEASING.md).
