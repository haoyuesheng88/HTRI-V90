# HTRI-V90

This repository stores reusable Codex skills and helper files for HTRI V9.0 workflows.

## Included Skill

- `skills/htri-xist-verify`
  Connect to an already open local HTRI Xchanger Suite window, open the Xist sample case, run it, and capture evidence.

## Install On Another Computer

1. Clone this repository.
2. Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-skill.ps1
```

3. Restart Codex if it is already open.

The installer copies the repository's `skills\` contents into `%USERPROFILE%\.codex\skills\`.

## Manual Install

Copy the folder below into your Codex skills directory:

```text
skills\htri-xist-verify
```

Default destination:

```text
%USERPROFILE%\.codex\skills\htri-xist-verify
```
