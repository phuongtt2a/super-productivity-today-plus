# Publishing Today+

Repository: https://github.com/phuongtt2a/super-productivity-today-plus

## Initial release

The first public release is `v0.2.0` to reflect the addition of paused-stopwatch manual time logging after the local `v0.1.0` prototype. A commit named `release: publish Today+ v0.2.0` triggers the release workflow on `main`.

The workflow validates and packages the four runtime files and creates a GitHub Release containing **`today-plus-super-productivity.zip`**. The GitHub-generated **Source code (zip)** is **not** installable as a plugin.

## Later releases

1. Bump `version` in `plugin/manifest.json` using semantic versioning.
2. Update `CHANGELOG.md`, README/screenshots when the interface changes, and run tests.
3. Commit changes to `main`.
4. Push a matching version tag (for example `v0.2.1`) to trigger GitHub Actions release packaging.
5. Verify the GitHub release URL, attached ZIP and matching manifest version.

Do not move already-published tags or silently overwrite release assets. Users should always install the ZIP attached to the latest Release.

GitHub About description, website, and topics are described in [ABOUT.md](ABOUT.md). They are separate from plugin manifest metadata.
