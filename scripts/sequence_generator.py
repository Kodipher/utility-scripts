from __future__ import annotations
from typing import Final, Iterable

import math
import random
from itertools import islice
from pathlib import Path
from traceback import format_exc


# == PROBLEM ==
# Given a list of sequence statements, generate those sequences


# ======== SETTINGS ======== #
# Length of the sequences
sequence_length: Final[int] = 50
# Number of places to round decimals to
round_decimals: Final[int] = 6

# Flag that dictates if the sequences should be printed to console
print_to_console: Final[bool] = True
# Filename to print sequences to or None for no file output
output_file: Final[str | None] = None

# Format of the whole output.
# Use {sequences} for main payload
output_format: Final[str] = "\n{sequences}\n\n"

# Format of the output for a single sequence.
# Use {sequence} for the sequence and {index} for sequence's index in the targets array.
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
# Sequences that need to be generated
sequences: Final[list[Iterable[float]]] = [
    seq_constant(value=5),
    seq_linear(start=5, shift=1.05)
]


# ======== GENERATION ======== #
def sequence_stringifier(sequence: Iterable[float], sequence_index: int) -> Iterable[str]:
    """
    Formats each sequence in according to sequence_format and element_separator.
    Does not process sequence values in any other way.
    """
    sequence_payload_string = element_separator.join(map(str, sequence))
    sequence_string = sequence_format.format(sequence=sequence_payload_string, index=sequence_index)
    return sequence_string

def main():

    # Generate sequences
    print("Generating sequences...")
    output_strings: list[str] = list()

    for i, sequence in enumerate(sequences):
        # Take rounding and length into account
        values = map(lambda x: round(x, round_decimals), islice(sequence, sequence_length))
        # Format and append to the result
        output_strings.append(sequence_stringifier(values, i))

    # Write file
    print("Forming output...")
    output_payload: str = output_format.format(sequences=sequence_separator.join(output_strings))

    print("Writing output...")
    # Write to file
    if output_file is not None:
        bytes_written = Path(output_file).write_text(output_payload)
        print(f"{bytes_written} bytes written to \"{output_file}\"")

    # Write to console
    if print_to_console:
        print("Generated sequences:")
        print(output_payload)


if __name__ == "__main__":
    try:
        main()
        input("Press enter to exit")
    except Exception:
        print("An error has occurred:")
        print(format_exc())
        input("Press enter to exit")
