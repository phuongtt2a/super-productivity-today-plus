# Releasing Today+

Repository: https://github.com/phuongtt2a/super-productivity-today-plus

## Latest release — v1.0.1

The current stable release is **v1.0.1**. The manifest, README, and release
version match. The earlier **v0.2.0** remains available as historical release
(we do not rewrite existing Git tags or ZIP assets).

A commit message beginning `release:` on `main`, or a matching version tag
(e.g. `v1.0.1`), triggers the GitHub Actions **Publish Today+ release** workflow.
The workflow validates and packages the four plugin files and creates a release
containing **`today-plus-super-productivity.zip`**.

**Do not download GitHub's automatic Source code (zip).** Install the
`today-plus-super-productivity.zip` file from the release Assets.

## Future releases

1. Edit and test the code. Bump `version` in `plugin/manifest.json` (e.g. to `1.0.2`).
2. Update the README, changelog and screenshots as needed.
3. Run `python -m unittest discover -s tests -p 'test_*.py' -v`.
4. Push a versioned commit or matching tag; let CI build the installable ZIP.
5. Verify tag, commit, asset checksum and the **Latest** release designation.

Never overwrite an older release's assets or move published tags to hide updates.

GitHub About description, website, and topics are documented in [ABOUT.md](ABOUT.md). They are separate from plugin manifest metadata.
