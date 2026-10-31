# Publishing Today+

Repository: https://github.com/phuongtt2a/super-productivity-today-plus

## Current version

**v1.1.0** adds nested subtasks, hides overdue and finished tasks by default, and introduces the **Not today** control to clear a due date without completing the task. The published v1.0.1 release remains available as historical reference; never overwrite an existing version tag or release asset.

## Publishing a new release

1. Update the version in `plugin/manifest.json`, README if necessary, and `CHANGELOG.md`.
2. Run the package and browser tests. Check the ZIP contains exactly four root files: `manifest.json`, `plugin.js`, `index.html`, `icon.svg`.
3. Refresh README screenshots when the UI changes.
4. Commit and push to `main` with a message beginning `release:`; the GitHub Action runs validation and publishes the version-matched release ZIP. Alternatively, push the corresponding `vX.Y.Z` tag.
5. Verify the GitHub Actions run and the release's `today-plus-super-productivity.zip` asset. Never tell users to install GitHub's automatic source archive.

## Same-version minor fixes

For small UI changes that intentionally **retain v1.1.0**, rebuild and commit `dist/today-plus-super-productivity.zip` on `main` alongside updated source, docs and screenshots. Do **not** use a `release:` commit message or move the existing version tag. The release attachment remains an immutable snapshot; link users to the installable ZIP on the current `main` branch for these fixes.

## Important constraints

- Keep the plugin identifier `sp-today-tasks-habits` unchanged so installed copies continue working.
- Verify the icon-only `Not today` action works on the first mouse click and mobile tap, including when the embedded view regains focus. It must only appear on tasks with a date to clear.
- Verify `Not today` clears `dueDay` and `dueWithTime` while leaving `isDone` unchanged. If clearing `dueWithTime`, also clear its related reminder when present.
- Recurring tasks require explicit user confirmation; modifying one occurrence's date may influence its repeat schedule.
- The native `Won't do` completion status is different from `Not today`. The plugin API does not support writing `wontDoOn`.
- Keep the GitHub About metadata suggestions in [ABOUT.md](ABOUT.md); the plugin manifest description is separate.
