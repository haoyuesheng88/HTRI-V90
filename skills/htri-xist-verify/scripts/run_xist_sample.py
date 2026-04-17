from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

try:
    from pywinauto import Application
    from pywinauto.findwindows import find_windows
except Exception as exc:  # pragma: no cover
    print(
        "pywinauto is required. Install it with: python -m pip install pywinauto",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


DEFAULT_SAMPLE = Path(
    r"C:\Program Files (x86)\HTRI\Xchanger Suite 9.0 - Hon\Samples\Xist_Sample.htri"
)
WINDOW_TITLE_RE = ".*HTRI Xchanger Suite.*"


def connect_main_window():
    handles = find_windows(title_re=WINDOW_TITLE_RE)
    if not handles:
        raise RuntimeError("No open HTRI Xchanger Suite window was found.")

    app = Application(backend="win32").connect(handle=handles[0])
    win = app.window(handle=handles[0])
    win.restore()
    win.set_focus()
    return app, win


def save_capture(win, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    win.capture_as_image().save(str(path))


def close_modal_dialogs(app) -> int:
    closed = 0
    for window in app.windows():
        try:
            if window.class_name() == "#32770":
                app.window(handle=window.handle).type_keys("{ESC}")
                closed += 1
        except Exception:
            continue
    return closed


def find_open_dialog(app):
    deadline = time.time() + 10
    while time.time() < deadline:
        for window in app.windows():
            try:
                if window.class_name() == "#32770":
                    return app.window(handle=window.handle)
            except Exception:
                continue
        time.sleep(0.2)
    raise RuntimeError("Open dialog did not appear.")


def open_sample(win, sample_path: Path) -> None:
    if sample_path.name in win.window_text():
        close_modal_dialogs(win.app)
        return

    win.type_keys("^o")
    dialog = find_open_dialog(win.app)

    edits = [c for c in dialog.children() if c.class_name() == "Edit"]
    if not edits:
        raise RuntimeError("Could not find the file name field in the Open dialog.")

    filename_edit = max(edits, key=lambda e: e.rectangle().top)
    filename_edit.click_input()
    filename_edit.set_edit_text(str(sample_path))

    buttons = [c for c in dialog.children() if c.class_name() == "Button"]
    if not buttons:
        raise RuntimeError("Could not find the Open button in the dialog.")

    buttons[0].click()

    deadline = time.time() + 20
    while time.time() < deadline:
        if sample_path.name in win.window_text():
            close_modal_dialogs(win.app)
            return
        time.sleep(0.5)
    raise RuntimeError("HTRI did not finish loading the Xist sample case.")


def run_case(win) -> None:
    # This coordinate targets the verified Run Case ribbon button relative to the main window.
    win.click_input(coords=(700, 82))


def current_status(win) -> str:
    try:
        statusbars = [c for c in win.children() if "StatusBar" in c.class_name()]
        if statusbars:
            return statusbars[0].window_text().strip()
    except Exception:
        pass
    return ""


def infer_success(win) -> bool:
    if DEFAULT_SAMPLE.name not in win.window_text():
        return False
    for window in win.app.windows():
        try:
            if window.class_name() == "#32770":
                return False
        except Exception:
            continue
    return True


def wait_for_completion(win, timeout_s: int) -> str:
    deadline = time.time() + timeout_s
    last_status = ""
    while time.time() < deadline:
        last_status = current_status(win)
        if "Run Completed" in last_status:
            return last_status
        time.sleep(1)
    return last_status or "Run requested; inspect xist-after-run.png"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Open the HTRI Xist sample case, run it, and capture evidence."
    )
    parser.add_argument(
        "--sample",
        default=str(DEFAULT_SAMPLE),
        help="Path to the Xist sample file.",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory for screenshots and logs.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Seconds to wait for run completion.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sample_path = Path(args.sample)
    output_dir = Path(args.output_dir).resolve()

    if not sample_path.exists():
        print(f"Sample file not found: {sample_path}", file=sys.stderr)
        return 1

    app, win = connect_main_window()
    save_capture(win, output_dir / "xist-before-open.png")
    open_sample(win, sample_path)
    save_capture(win, output_dir / "xist-after-open.png")
    close_modal_dialogs(app)
    run_case(win)
    status = wait_for_completion(win, args.timeout)
    save_capture(win, output_dir / "xist-after-run.png")
    ok = infer_success(win)

    print(f"sample={sample_path}")
    print(f"output_dir={output_dir}")
    print(f"status={status or 'UNKNOWN'}")
    print(f"success={'yes' if ok else 'no'}")
    print(f"artifacts={output_dir / 'xist-before-open.png'}")
    print(f"artifacts={output_dir / 'xist-after-open.png'}")
    print(f"artifacts={output_dir / 'xist-after-run.png'}")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
