# Releasing

Only the owner releases. Agents never tag, publish or create a release.

## What a release is here

A release is a git tag on `main` plus a GitHub release with the notes from `CHANGELOG.md`. The project is a standard-library Python package run from a checkout, so there is no package registry upload and no build artefact. No release exists yet, and nothing can be released before the walking skeleton (ticket #2) is merged.

## Before tagging

1. `main` is green in CI on Linux and Windows.
2. On a clean checkout of `main`: `python -m unittest` exits 0 (command introduced by ticket #2).
3. The commands in `README.md` and `CLAUDE.md` run as written; none is still marked planned.
4. `CHANGELOG.md`: rename `Unreleased` to the version and date, and start a new empty `Unreleased`. Commit through a pull request.
5. The licence is still unselected. Do not publish a release that implies one; ask the owner first (`README.md`, "Licensing").

## Tagging

1. From an up-to-date `main`: `git tag -a vX.Y.Z -m "vX.Y.Z"` and `git push origin vX.Y.Z`.
2. Create the GitHub release from the tag with the changelog section as notes.
3. Pre-1.0 versions: increment the minor version for a change to the scenario or replay schema, otherwise the patch version. A schema change must already have bumped the schema version (see `docs/architecture.md`).
