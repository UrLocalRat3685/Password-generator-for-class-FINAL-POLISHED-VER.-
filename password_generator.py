"""
My awesome password generator!! ^_^
----------------------------------
Two types:
1) Memorable  -> words + 1 digit each + hyphens
2) Random     -> characters from chosen sets

Logs passwords + timestamps into:
  Memorable/Generated_Passwords.txt
  Random/Generated_Passwords.txt
"""

import random
import string
from datetime import datetime
from pathlib import Path
from typing import List


WORDLIST_FILENAME = "top_english_nouns_lower_100000.txt"


# -----------------------------
# helpers :D
# -----------------------------
def vibe_timestamp() -> str:
    return datetime.now().strftime("%a %Y-%m-%d %H:%M:%S")


def make_dirs_if_missing() -> None:
    Path("Memorable").mkdir(parents=True, exist_ok=True)
    Path("Random").mkdir(parents=True, exist_ok=True)


def log_password(folder: str, password: str) -> None:
    make_dirs_if_missing()
    log_path = Path(folder) / "Generated_Passwords.txt"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"{vibe_timestamp()} | {password}\n")


def load_words(wordlist_path: str = WORDLIST_FILENAME) -> List[str]:
    p = Path(wordlist_path)
    if not p.exists():
        raise FileNotFoundError(
            f"Missing '{wordlist_path}'. Place '{WORDLIST_FILENAME}' next to this script."
        )

    with p.open("r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]

    if len(words) < 100:
        raise ValueError("Word list looks invalid or too small.")
    return words


def apply_case(word: str, case_style: str) -> str:
    style = case_style.lower()
    if style == "lower":
        return word.lower()
    if style == "upper":
        return word.upper()
    if style in ("title", "capitalize"):
        return word.capitalize()
    if style == "random":
        return "".join(
            ch.upper() if random.choice([True, False]) else ch.lower()
            for ch in word
        )
    raise ValueError("Case must be: lower, upper, title, or random")


# -----------------------------
# password generators
# -----------------------------
def generate_memorable_password(
    num_words: int = 3,
    case_style: str = "title",
    wordlist_path: str = WORDLIST_FILENAME,
) -> str:
    if not (2 <= num_words <= 10):
        raise ValueError("num_words should be between 2 and 10.")

    words = load_words(wordlist_path)
    chosen = random.sample(words, k=num_words)

    parts = []
    for w in chosen:
        styled = apply_case(w, case_style)
        digit = str(random.randint(0, 9))
        parts.append(styled + digit)

    return "-".join(parts)


def build_allowed_characters(
    use_lower: bool,
    use_upper: bool,
    use_digits: bool,
    use_punct: bool,
    excluded: str = "",
) -> str:
    pool = ""
    if use_lower:
        pool += string.ascii_lowercase
    if use_upper:
        pool += string.ascii_uppercase
    if use_digits:
        pool += string.digits
    if use_punct:
        pool += string.punctuation

    pool = "".join(ch for ch in pool if ch not in excluded)

    if not pool:
        raise ValueError("No characters left after exclusions.")
    return pool


def generate_random_password(
    length: int = 16,
    use_lower: bool = True,
    use_upper: bool = True,
    use_digits: bool = True,
    use_punct: bool = False,
    excluded: str = "",
) -> str:
    if not (4 <= length <= 128):
        raise ValueError("length must be between 4 and 128.")

    pool = build_allowed_characters(
        use_lower, use_upper, use_digits, use_punct, excluded
    )
    return "".join(random.choice(pool) for _ in range(length))


# -----------------------------
# input helpers
# -----------------------------
def ask_yes_no(msg: str) -> bool:
    while True:
        ans = input(f"{msg} (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please enter y or n :3")


def ask_int(msg: str, min_val: int, max_val: int) -> int:
    while True:
        try:
            val = int(input(msg).strip())
            if min_val <= val <= max_val:
                return val
            print(f"Enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("That's not a number, try again :3")


# -----------------------------
# modes
# -----------------------------
def interactive_mode() -> None:
    print("\n=== Password Generator :3 ===")
    print("1) Memorable")
    print("2) Random")
    choice = input("Choose 1 or 2: ").strip()

    if choice == "1":
        num_words = ask_int("How many words (2-10): ", 2, 10)
        print("Case options: lower, upper, title, random")
        case_style = input("Case style: ").strip()

        pwd = generate_memorable_password(num_words, case_style)
        print(f"\nGenerated memorable password: {pwd} :3")
        log_password("Memorable", pwd)

    elif choice == "2":
        length = ask_int("Password length (4-128): ", 4, 128)
        use_punct = ask_yes_no("Include punctuation?")
        excluded = input("Characters to exclude (Enter for none): ")

        pwd = generate_random_password(
            length=length,
            use_punct=use_punct,
            excluded=excluded,
        )
        print(f"\nGenerated random password: {pwd} :3")
        log_password("Random", pwd)

    else:
        print("Invalid choice. Run it back :3")


def verify_generate_1000() -> None:
    make_dirs_if_missing()
    print("\nGenerating 1000 passwords to verify logging... :3")

    for i in range(1, 1001):
        if random.choice([True, False]):
            pwd = generate_memorable_password(
                num_words=random.randint(2, 5),
                case_style=random.choice(["lower", "upper", "title", "random"]),
            )
            log_password("Memorable", pwd)
        else:
            pwd = generate_random_password(
                length=random.randint(10, 24),
                use_punct=random.choice([True, False]),
            )
            log_password("Random", pwd)

        if i % 200 == 0:
            print(f"{i}/1000 complete :3")

    print("Done! All passwords logged successfully :3")


def main() -> None:
    print("=== Derick Password Generator :3 ===")
    print("1) Interactive mode")
    print("2) Generate 1000 passwords (verification)")
    mode = input("Choose 1 or 2: ").strip()

    try:
        if mode == "1":
            interactive_mode()
        elif mode == "2":
            verify_generate_1000()
        else:
            print("Invalid option :3")
    except Exception as e:
        print(f"Error: {e}")
        print("Check your word list file name/location :3")


if __name__ == "__main__":
    main()
