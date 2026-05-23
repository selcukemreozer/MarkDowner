#!/usr/bin/env python3
"""
File to Markdown Converter CLI
A terminal-based CLI tool that converts various file types to Markdown format.
Uses Microsoft's markitdown library for conversion.
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple

import inquirer
from markitdown import MarkItDown


def get_all_files(directory: str = ".") -> List[str]:
    """Get all files in the given directory (non-recursive), excluding hidden files."""
    files = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) and not item.startswith("."):
            files.append(item)
    return sorted(files)


def get_subdirectories(directory: str = ".") -> List[str]:
    """Get all sub-directories in the given directory, excluding hidden ones."""
    dirs = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path) and not item.startswith("."):
            dirs.append(item)
    return sorted(dirs)


def display_menu() -> str:
    """Display the main menu and return the user's choice."""
    questions = [
        inquirer.List(
            "action",
            message=f"Current directory: {os.getcwd()}",
            choices=["Convert files to Markdown", "Change directory", "Exit"],
        ),
    ]
    answers = inquirer.prompt(questions)
    if not answers:
        return "Exit"
    return answers["action"]


def change_directory() -> None:
    """Browse and change the working directory interactively."""
    while True:
        subdirs = get_subdirectories()
        choices = [".. (parent directory)"] + subdirs + ["[ Stay here ]"]
        questions = [
            inquirer.List(
                "target",
                message=f"Navigate from: {os.getcwd()}",
                choices=choices,
            ),
        ]
        answers = inquirer.prompt(questions)
        if not answers or answers["target"] == "[ Stay here ]":
            return

        target = answers["target"]
        if target == ".. (parent directory)":
            os.chdir("..")
        else:
            os.chdir(target)


def select_files(files: List[str]) -> List[str]:
    """Allow the user to select multiple files from the list."""
    questions = [
        inquirer.Checkbox(
            "selected_files",
            message="Select files (SPACE to toggle, ENTER to confirm)",
            choices=files,
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers["selected_files"] if answers else []


def convert_file(
    converter: MarkItDown, file_path: str, output_dir: str = "converted"
) -> Tuple[bool, str]:
    """Convert a single file to Markdown. Returns (success, message_or_path)."""
    try:
        Path(output_dir).mkdir(exist_ok=True)
        output_path = os.path.join(output_dir, f"{Path(file_path).stem}.md")
        result = converter.convert(file_path)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.text_content)
        return True, output_path
    except Exception as e:
        return False, str(e)


def main() -> None:
    """Main CLI application loop."""
    print("\n" + "=" * 50)
    print("    File to Markdown Converter (markitdown)")
    print("=" * 50 + "\n")

    converter = MarkItDown()

    while True:
        action = display_menu()

        if action == "Exit":
            print("\nGoodbye!")
            return

        if action == "Change directory":
            change_directory()
            continue

        files = get_all_files()
        if not files:
            print("\nNo files found in the current directory.\n")
            continue

        print(f"\nFound {len(files)} file(s) in the current directory.\n")
        selected_files = select_files(files)

        if not selected_files:
            print("\nNo files selected.\n")
            continue

        print(f"\nConverting {len(selected_files)} file(s)...\n")
        successful = 0
        failed = 0

        for file_name in selected_files:
            ok, result = convert_file(converter, file_name)
            if ok:
                print(f"  [OK]   {file_name} -> {result}")
                successful += 1
            else:
                print(f"  [FAIL] {file_name} - {result}")
                failed += 1

        print(f"\n{'=' * 50}")
        print("Conversion complete!")
        print(f"  Successful: {successful}")
        print(f"  Failed:     {failed}")
        print("  Output directory: ./converted")
        print(f"{'=' * 50}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)
