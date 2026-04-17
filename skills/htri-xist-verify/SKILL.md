---
name: htri-xist-verify
description: Connect to an already open local HTRI Xchanger Suite window and verify Xist by opening a simple sample case, running it, and capturing evidence. Use when the user asks to connect to HTRI, verify a local XIST installation, open a sample or test case in Xist, or prove that HTRI can run end-to-end on this Windows machine.
---

# HTRI XIST Verify

Use this skill to validate a local HTRI Xist installation quickly and repeatably.

## Quick Start

1. Confirm an HTRI main window is already open.
2. Prefer the bundled script:

```powershell
python "<skill-dir>\scripts\run_xist_sample.py"
```

3. Review the printed artifact paths and the final status.

## Workflow

1. Connect to the existing `HtriGui.exe` window with `pywinauto`.
2. Open the installed sample file:

```text
C:\Program Files (x86)\HTRI\Xchanger Suite 9.0 - Hon\Samples\Xist_Sample.htri
```

3. Trigger `Run Case`.
4. Capture screenshots before and after the run.
5. Report whether the window shows `Run Completed` and whether the output summary is visible.

## Notes

- Assume Windows and PowerShell.
- Assume HTRI is already installed and open unless the user says otherwise.
- If `pywinauto` is missing, install it with `python -m pip install pywinauto`.
- HTRI is a 32-bit app; `pywinauto` from 64-bit Python can still work, but expect warnings.
- If the user specifically asks for a public online case, keep the sample-run path for fast validation first, then optionally look up a public case afterward.
- Do not close the user's existing HTRI session unless asked.

## Script

- Main automation entrypoint: [scripts/run_xist_sample.py](scripts/run_xist_sample.py)
- The script writes artifacts to the current working directory by default.
- Resolve `<skill-dir>` to the installed `htri-xist-verify` folder under `%USERPROFILE%\.codex\skills\` unless your `CODEX_HOME` is customized.
