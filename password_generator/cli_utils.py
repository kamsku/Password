import os
import sys
import time
from typing import List, Optional

def enable_ansi_on_windows() -> bool:
    if os.name != "nt":
        return True

    try:
        import colorama
        colorama.just_fix_windows_console()
        return True
    except ImportError:
        pass
    except Exception as e:
        print(f"Warning: Colorama failed to initialize: {e}", file=sys.stderr)

    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        h_stdout = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE = -11
        mode = ctypes.c_uint()
        if kernel32.GetConsoleMode(h_stdout, ctypes.byref(mode)) == 0:
            return False
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
        if kernel32.SetConsoleMode(h_stdout, new_mode) == 0:
            return False
        return True
    except Exception as e:
        print(f"Warning: ctypes ANSI enablement failed: {e}", file=sys.stderr)
        return False


USE_COLOR = enable_ansi_on_windows()

ANSI = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "cyan": "\033[36m",
}

# If there is no ANSI support, we turn off the codes
if not USE_COLOR:
    ANSI = {k: "" for k in ANSI}

def c(text: str, color: str) -> str:
    """Returns text with ANSI color codes if supported."""
    return f"{ANSI.get(color,'')}{text}{ANSI['reset']}"

def print_header(title_text: str) -> None:
    """Prints a formatted application header."""
    line = "═" * (len(title_text) + 2)
    print(c(f"\n{line}\n {title_text}\n{line}", "cyan"))

def print_menu(options: List[str]) -> None:
    """Prints a menu of options."""
    print(c("\nWybierz opcję:", "bold"))
    for i, option in enumerate(options, 1):
        print(f"  {i}) {option}")

def prompt_int(label: str, default: int, min_value: int = 1, max_value: Optional[int] = None) -> int:
    """Prompts the user for an integer with validation."""
    while True:
        raw = input(f"{label} [{default}]: ").strip()
        if not raw:
            value = default
        else:
            try:
                value = int(raw)
            except ValueError:
                print(c("Please enter an integer.", "red"))
                continue

        if value < min_value:
            print(c(f"Value must be >= {min_value}.", "red"))
            continue
        if max_value is not None and value > max_value:
            print(c(f"Value must be <= {max_value}.", "red"))
            continue
        return value

def prompt_choice(label: str, choices: List[str], default: str) -> str:
    """Prompts the user to choose from a list of options."""
    choices_lower = [x.lower() for x in choices]
    default_lower = default.lower()

    while True:
        raw = input(f"{label} {choices} [{default}]: ").strip().lower()
        if not raw:
            raw = default_lower
        if raw in choices_lower:
            return choices[choices_lower.index(raw)]
        print(c(f"Invalid choice. Available: {choices}", "red"))

def pause() -> None:
    """Waits for the user to press Enter."""
    input(c("\nPress Enter to return to menu...", "dim"))

def display_error(message: str) -> None:
    """Displays an error message in red."""
    print(c(f"Error: {message}", "red"))
    pause()

def display_success(message: str) -> None:
    """Displays a success message in green."""
    print(c(message, "green"))

def display_info(message: str) -> None:
    """Displays an informational message."""
    print(c(message, "dim"))