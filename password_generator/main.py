import logging
from getpass import getpass
from pathlib import Path
from typing import List, Dict, Any, Callable
import pandas as pd
from dataclasses import dataclass

from cli_utils import c, print_header, print_menu, prompt_int, prompt_choice, pause, display_error, display_success, display_info
from config import (
    DEFAULT_PASSWORD_LENGTH,
    DEFAULT_PASSWORDS_COUNT,
    DEFAULT_OUTPUT_CSV,
    DEFAULT_OUTPUT_XLSX,
    BCRYPT_ROUNDS,
)
from password_generator import PasswordGenerator, PasswordValidationError
from hashing_functions import HashFunctions
from timing_utils import measure_ms


@dataclass(frozen=True)
class AlgorithmSpec:
    name: str
    func: Callable[[str], Any]
    repeat: int = 1  # how many times to repeat the measurement for a more stable result


def build_algorithms() -> List[AlgorithmSpec]:
    """Creates a list of hashing algorithm specifications for analysis."""
    fast_repeat = 5000

    return [
        AlgorithmSpec("MD5", HashFunctions.md5_hex, repeat=fast_repeat),
        AlgorithmSpec("SHA-1", HashFunctions.sha1_hex, repeat=fast_repeat),
        AlgorithmSpec("SHA-256", HashFunctions.sha256_hex, repeat=fast_repeat),
        AlgorithmSpec("SHA-512", HashFunctions.sha512_hex, repeat=fast_repeat),
        AlgorithmSpec("bcrypt", HashFunctions.bcrypt_hex, repeat=1),
        AlgorithmSpec("scrypt", HashFunctions.scrypt_hex, repeat=1),
    ]


def run_analysis(passwords_count: int, password_length: int) -> pd.DataFrame:
    """Generates passwords, hashes them with various algorithms, and measures execution times."""
    logging.info(f"Generating {passwords_count} passwords (length={password_length})...")
    passwords = PasswordGenerator.generate_batch(passwords_count, password_length)

    algorithms = build_algorithms()
    logging.info("Algorithms: " + ", ".join(a.name for a in algorithms))

    results: List[Dict[str, Any]] = []

    for idx, pwd in enumerate(passwords, start=1):
        record: Dict[str, Any] = {"ID": idx, "Password": pwd, "Length": len(pwd)}

        for algo in algorithms:
            out, ms = measure_ms(algo.func, pwd, repeat=algo.repeat)

            # bcrypt/scrypt return tuples
            if algo.name == "bcrypt":
                hash_hex, hash_str = out
                record[f"{algo.name}_hash_hex"] = hash_hex
                record[f"{algo.name}_hash_str"] = hash_str
            elif algo.name == "scrypt":
                hash_hex, salt_hex = out
                record[f"{algo.name}_hash_hex"] = hash_hex
                record[f"{algo.name}_salt_hex"] = salt_hex
            else:
                record[f"{algo.name}_hash_hex"] = out

            record[f"{algo.name}_time_ms"] = ms

        results.append(record)

    df = pd.DataFrame(results)
    return df


def export_results(df: pd.DataFrame, export_format: str, csv_path: str, xlsx_path: str) -> None:
    """Exports analysis results to CSV and/or XLSX files."""
    export_format = export_format.lower()

    if export_format in ("csv", "both"):
        Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        logging.info(f"CSV saved: {csv_path}")

    if export_format in ("xlsx", "both"):
        Path(xlsx_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(xlsx_path, index=False)
        logging.info(f"XLSX saved: {xlsx_path}")


def print_summary(df: pd.DataFrame) -> None:
    """Prints a summary of average hashing times."""
    time_cols = [col for col in df.columns if col.endswith("_time_ms")]
    if not time_cols:
        return

    means = df[time_cols].mean(numeric_only=True).sort_values()
    print(c("\nAverage times (ms) for algorithms:", "bold"))
    for col, val in means.items():
        algo = col.replace("_time_ms", "")
        print(f"  - {algo:8s}: {val:.4f} ms")


def option_batch_analysis() -> None:
    """Handles the menu option: Batch analysis (N passwords) + CSV/XLSX export."""
    print(c("\n[Batch Analysis]", "bold"))

    count = prompt_int("Enter number of passwords", DEFAULT_PASSWORDS_COUNT, min_value=1, max_value=100_000)
    length = prompt_int("Enter password length", DEFAULT_PASSWORD_LENGTH, min_value=4, max_value=256)

    try:
        df = run_analysis(count, length)
        print_summary(df)

        export_choice = prompt_choice("Export", ["csv", "xlsx", "both", "none"], default="csv")

        if export_choice != "none":
            csv_path = DEFAULT_OUTPUT_CSV
            xlsx_path = DEFAULT_OUTPUT_XLSX

            if export_choice in ("csv", "both"):
                csv_path = input(f"CSV file name [{DEFAULT_OUTPUT_CSV}]: ").strip() or DEFAULT_OUTPUT_CSV
            if export_choice in ("xlsx", "both"):
                xlsx_path = input(f"XLSX file name [{DEFAULT_OUTPUT_XLSX}]: ").strip() or DEFAULT_OUTPUT_XLSX

            export_results(df, export_choice, csv_path, xlsx_path)
        else:
            display_info("Export skipped.")

    except (PasswordValidationError, RuntimeError, Exception) as e:
        display_error(str(e))
    finally:
        pause()


def option_generate_one() -> None:
    """Handles the menu option: Generate a single password."""
    print(c("\n[Single Password Generator]", "bold"))
    length = prompt_int("Enter password length", DEFAULT_PASSWORD_LENGTH, min_value=4, max_value=256)
    try:
        pwd = PasswordGenerator.generate_one(length)
        print(c("\nGenerated password:", "bold"))
        display_success(pwd)
    except PasswordValidationError as e:
        display_error(str(e))
    finally:
        pause()


def option_hash_user_password() -> None:
    """Handles the menu option: Hash user-entered password."""
    print(c("\n[Hash User Password]", "bold"))
    display_info("Password will be entered hidden (will not show in terminal).")

    pwd = getpass("Enter password: ")
    if not pwd:
        display_info("Empty password - canceled.")
        pause()
        return

    algorithms = build_algorithms()
    names = [a.name for a in algorithms]

    print("\nAvailable algorithms:", ", ".join(names))
    choice = prompt_choice("Select algorithm", names + ["ALL"], default="ALL")

    selected_algorithms = algorithms if choice == "ALL" else [a for a in algorithms if a.name == choice]

    print(c("\nResults:", "bold"))
    for algo in selected_algorithms:
        try:
            out, ms = measure_ms(algo.func, pwd, repeat=algo.repeat)

            print(c(f"\n{algo.name}", "cyan"))
            if algo.name == "bcrypt":
                hash_hex, hash_str = out
                print(f"  hash_hex : {hash_hex}")
                print(f"  hash_str : {hash_str}")
            elif algo.name == "scrypt":
                hash_hex, salt_hex = out
                print(f"  hash_hex : {hash_hex}")
                print(f"  salt_hex : {salt_hex}")
            else:
                print(f"  hash_hex : {out}")

            print(f"  time_ms  : {ms:.4f}")
        except Exception as e:
            print(c(f"  Error hashing {algo.name}: {e}", "red"))
    pause()


def main() -> None:
    """Main application function, handling menu and option selection."""
    menu_options = [
        "Batch analysis (N passwords) + CSV/XLSX export",
        "Generate a single password (user chooses length)",
        "Hash user-entered password",
        "Exit",
    ]

    while True:
        print_header("Password Generator + Hashing/Timing + Export")
        print_menu(menu_options)

        choice = input("\nYour choice [1-4]: ").strip()
        if choice == "1":
            option_batch_analysis()
        elif choice == "2":
            option_generate_one()
        elif choice == "3":
            option_hash_user_password()
        elif choice == "4":
            display_success("\nGoodbye!")
            break
        else:
            display_error("Invalid choice.")
            time.sleep(0.6)


if __name__ == "__main__":
    main()