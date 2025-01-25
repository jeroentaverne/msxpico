#!/usr/bin/env python3
"""
Author: Pax-NL
Description: A script for creating the selection.cat for the menu of the MSX Pico cardridge
"""
import os
import sys
import struct
import argparse
from typing import List

# Version 1.0 - Initial version
# Version 1.1 - Added alphabetical sorting for .rom files
# Version 1.2 - Fixed output directory location
# Version 1.3 - Fixed output file location based
# Version 1.4 - Added --version and --help

FILENAME_SIZE: int = 256
ENTRY_SIZE: int = 96
NAME_SIZE: int = 80
SIZE_POS: int = 80
MAPPER_POS: int = 84
GEN_POS: int = 86

# Define the maximum lengths for each field for ASCII table
MAX_NAME_LENGTH = 40
MAX_MAPPER_LENGTH = 10
MAX_GENERATION_LENGTH = 10
MAX_SIZE_LENGTH = 10

mapper_table: List[str] = [
    "generic8",
    "generic16",
    "konami5",
    "konami4",
    "ascii8",
    "ascii16",
    "gamemaster2",
    "fmpac",
    "ascii16ex",
    "rtype",
    "nextor_ram",
    "disk",
    "plain0000",
    "plain4000",
    "plain8000",
    "neo16",
    "neo8",
    "konamiultimate",
]

msxgen_table: List[str] = ["msx1", "msx2", "msx2+", "turbor"]


def search_table(text: str, table: List[str]) -> int:
    """
    Search for a string in a table.

    Args:
        text: The text to search for.
        table: The list of strings to search in.

    Returns:
        The index of the first occurrence of the text in the table, or 0 if not found.
    """
    for i, item in enumerate(table):
        p = text.find("_")
        if p != -1:
            len_table_i = len(item)
            p = text.find(item, p)
            if p != -1 and (
                text[p + len_table_i] == "_" or text[p + len_table_i] == "."
            ):
                return i
    return 0


def print_header():
    """
    Print ASCII table style header lines.
    """
    print(
        "",
        "-" * (MAX_NAME_LENGTH + 2),
        "-" * (MAX_MAPPER_LENGTH + 2),
        "-" * (MAX_GENERATION_LENGTH + 2),
        "-" * (MAX_SIZE_LENGTH + 2),
    )


def print_summary(filecount: int, skipcount: int, output_path: str) -> None:
    """
    Print summary of files added, skipped, and output file size.
    """
    print_header()

    # Find the maximum length among the numbers
    max_length = max(
        len(str(filecount)),
        len(str(skipcount)),
        len(str(os.path.getsize(output_path))),
        len(str(output_path)),
    )

    summary_info = [
        f"| Files added      : {filecount:>{max_length}} |",
        f"| Files skipped    : {skipcount:>{max_length}} |",
        f"| Output file size : {os.path.getsize(output_path):>{max_length}} |",
        f"| Output file name : {output_path:>{max_length}} |",
    ]

    for info in summary_info:
        print(info)

    print(" ---------------------" + "-" * (max_length))


def main() -> None:
    """
    Main function to process ROM files.
    """
    parser = argparse.ArgumentParser(description="Process ROM files.")
    parser.add_argument(
        "roms_path", metavar="<ROMs path>", type=str, help="path to the ROMs directory"
    )
    parser.add_argument(
        "output_file", metavar="<output file>", type=str, help="output file name"
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.4")
    args = parser.parse_args()

    if not os.path.isdir(args.roms_path):
        print("Error: Invalid ROMs directory.")
        sys.exit(1)

    # Get the output directory and file name
    output_directory, output_file = os.path.split(os.path.abspath(args.output_file))

    # Change to the specified ROMs directory
    os.chdir(args.roms_path)

    # Initialize variables
    filecount: int = 0
    skipcount: int = 0

    # Sorting .rom files alphabetically
    rom_files: List[str] = sorted(
        [direntp for direntp in os.listdir(".") if direntp.lower().endswith(".rom")]
    )

    # Build the full path for the output file
    output_path: str = os.path.join(output_directory, output_file)

    # Print the header
    print_header()
    print(
        f"| {'Name':<{MAX_NAME_LENGTH}} | {'Mapper':<{MAX_MAPPER_LENGTH}} | {'Generation':>{MAX_GENERATION_LENGTH}} | {'Size':<{MAX_SIZE_LENGTH}} |"
    )
    print_header()

    # Open the output file in binary write mode
    with open(output_path, "wb") as f_output:
        # Write the header
        f_output.write(b"MSXPICO_ROM_CAT\x00")

        # Iterate through the sorted .rom files
        for name in rom_files:
            name = name[:FILENAME_SIZE]
            filename = name

            # Extract information from the ROM file name
            filesize: int = 0
            mapper: int = search_table(name.lower(), mapper_table)
            msxgen: int = search_table(name.lower(), msxgen_table)

            with open(filename, "rb") as f_input:
                filesize = os.path.getsize(filename)
                filesize = (filesize + 15) & 0xFFFFFFF0
                buffer = bytearray(f_input.read(filesize))

            p = name.find("_")
            if p != -1:
                name = name[:p]

            # Check if mapper and generation are valid
            if mapper > 0 and msxgen <= 3:
                # Print the data with fixed widths
                print(
                    f"| {name[:MAX_NAME_LENGTH]:<{MAX_NAME_LENGTH}} | {mapper_table[mapper]:<{MAX_MAPPER_LENGTH}} | {msxgen_table[msxgen]:>{MAX_GENERATION_LENGTH}} | {filesize:>{MAX_SIZE_LENGTH}} |"
                )

                # Create entry and pack information
                entry = bytearray(ENTRY_SIZE)
                entry[: len(name)] = name.encode("ascii")
                struct.pack_into("<I", entry, SIZE_POS, filesize)
                entry[MAPPER_POS] = mapper
                entry[GEN_POS] = msxgen

                # Write entry and buffer to output file
                f_output.write(entry)
                f_output.write(buffer)

                filecount += 1
            else:
                print(f"Name: {name} Mapper or generation not specified, skipped!")
                skipcount += 1

        # Write a blank entry to mark the end of the file list
        entry = bytearray(ENTRY_SIZE)
        f_output.write(entry)

    # Print summary
    print_summary(filecount, skipcount, output_path)


if __name__ == "__main__":
    main()
