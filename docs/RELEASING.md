# Publishing Today+

Repository: https://github.com/phuongtt2a/super-productivity-today-plus

## Workflow: issue → PR → merge → published ZIP

1. Track bugs and enhancements in GitHub Issues.
2. Work in an issue-linked branch and open a pull request. CI checks the package and source; it does **not** publish from PR branches.
3. Review, test and merge the PR into `main`.
4. The **Publish Today+ release** GitHub Action runs automatically after every successful merge to `main`. It runs the tests and builds the four-file ZIP before publishing.
5. Check the GitHub Actions run and download the installable ZIP from [Latest Release](https://github.com/phuongtt2a/super-productivity-today-plus/releases/latest). Never install GitHub's automatically generated **Source code** archives.

No manual deletion or replacement of release attachments is required for normal releases.

## Minor changes with the same version

- Leave `plugin/manifest.json` at its current version (for example `1.1.0`).
- After merge, the Action compares the new ZIP with the Release asset. If identical, it does nothing. If different, it backs up the previous asset, replaces the ZIP using `gh release upload --clobber`, then downloads and byte-compares the uploaded ZIP.
- The version and its existing Git tag remain unchanged. The release notes record the updated ZIP's source commit and SHA-256 so the refreshed build is traceable.
- GitHub's automatic source archives continue to refer to the **original version tag**, which may not match the latest ZIP. Users should always install `today-plus-super-productivity.zip` from **Assets**.
- If GitHub release immutability is enabled, updating an old release is not allowed; publish a new version instead. Do not work around that protection.

## New version

1. Update `plugin/manifest.json`, `CHANGELOG.md`, and user-facing documentation as needed.
2. Run the test suite and update screenshots for interface changes.
3. Merge through a PR to `main`. If no release exists for the new `vX.Y.Z`, the Action creates a version-matched tag and GitHub Release with the tested ZIP.
4. Verify the Action succeeds and the Release asset is installable.

## Safeguards

- Publishing runs **only for `main`** (or an explicit manual workflow run targeting `main`), never for PRs.
- Separate publication runs are serialized, and the Action exits on failed tests.
- Before replacing an asset, the previous version is downloaded as a rollback copy. Upload failures attempt to restore it. Since `--clobber` deletes first, there can be a short gap if the replacement upload fails.
- After publishing, the Action downloads the ZIP and checks that its bytes match the tested build.
- Keep the plugin ID `sp-today-tasks-habits` unchanged to preserve installed plugin identity.
- The native **Won't do** status differs from Today+'s **Not Today** (clear scheduled date). The Plugin API does not currently expose native `wontDoOn` updates.
