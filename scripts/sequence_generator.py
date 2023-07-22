from __future__ import annotations
from typing import Final, Iterable

import math
import random
from pathlib import Path
from traceback import format_exc


# == PROBLEM ==
# Given a list of sequence statements, generate those sequences


# ======== SETTINGS ======== #
# Length of the sequences
sequence_length: Final[int] = 50
# Number of places to round decimals to
round_decimals: Final[int] = 6

# Flag that dictates if the sequences should be print to console
print_to_console: Final[bool] = True
# Filename to print sequences to or None for no file output
output_file: Final[str | None] = None

# Format of the output for a single sequence. Supports {index} and {sequence}.
sequence_format: Final[str] = "!{sequence}"
# Separators between sequences and sequence elements
sequence_separator: Final[str] = "\n\n"
element_separator: Final[str] = ", "

# Sequences are set in the targets selection below


# ======== SEQUENCES ======== #
def seq_constant(value: float) -> Iterable[float]:
    while True:
        yield value

def seq_linear(start: float, shift: float) -> Iterable[float]:
    val = start
    while True:
        yield val
        val = val + shift


# ======== TARGETS ======== #
sequences: Final[list[Iterable[float]]] = [
    seq_constant(value=5),
    seq_linear(start=5, shift=1.05)
]


# ======== GENERATION ======== #
def main():
    pass


if __name__ == "__main__":
    try:
        main()
        input("Press enter to exit")
    except Exception:
        print("An error has occurred:")
        print(format_exc())
        input("Press enter to exit")
