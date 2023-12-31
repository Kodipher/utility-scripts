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
sequence_length: Final[int] = 20
# Number of places to round decimals to
round_decimals: Final[int] = 6

# Flag that dictates if the sequences should be printed to console
print_to_console: Final[bool] = True
# Filename to print sequences to or None for no file output
output_file: Final[str | None] = "generated_sequences.txt"

# Format of the whole output.
# Use {sequences} for main payload
output_format: Final[str] = "\n# == BEGIN SEQUENCES ==\n\n{sequences}\n\n"

# Format of the output for a single sequence.
# Use {sequence} for the sequence and {index} for sequence's index in the targets array.
sequence_format: Final[str] = "seq{index} = [ {sequence} ]"

# Format of the comment line. Use {text} for actual comment text.
comment_format: Final[str] = "# {text}"

# Separators between sequences, sequence elements and comment lines for a sequence
sequence_separator: Final[str] = "\n\n"
element_separator: Final[str] = ", "
comment_separator: Final[str] = "\n"

# Separator between sequence and it's comments
separator_between_comment_and_sequence: Final[str] = "\n"

# Sequences are set in the targets selection below


# ======== SEQUENCES ======== #
class SequenceInstance:

    values: Iterable[float]
    comments: Iterable[str]

    def __init__(self, values: Iterable[float], *comments):
        self.values = values
        self.comments = comments


def seq_constant(value: float) -> SequenceInstance:
    def gen():
        while True:
            yield value
    return SequenceInstance(gen(), f"Constant; value {value}")


def seq_linear(start: float, shift: float) -> SequenceInstance:
    def gen():
        val = start
        while True:
            yield val
            val = val + shift
    return SequenceInstance(gen(), f"Linear; start {start} shift {shift}")


def seq_mult(start: float, mult: float) -> SequenceInstance:
    def gen():
        val = start
        while True:
            yield val
            val = val * mult
    return SequenceInstance(gen(), f"Multiplication; start {start}, multiplier {mult}")


def seq_power(base: float, exp_start: float = 0, exp_shift: float = 1) -> SequenceInstance:
    def gen():
        exp = exp_start
        while True:
            yield base**exp
            exp = exp + exp_shift
    return SequenceInstance(gen(), f"Power; base {base}, exponent start {exp_start}, exponent shift {exp_shift}")


def seq_lucas(first: float, second: float) -> SequenceInstance:
    def gen():
        first_copy = first
        second_copy = second
        yield first_copy
        yield second_copy
        while True:
            third = first_copy + second_copy
            yield third
            first_copy = second_copy
            second_copy = third
    return SequenceInstance(gen(), f"Lucas/Fibonachi; first {first}, second {second}")


def seq_mod_alt_sign(sequence: SequenceInstance, is_start_negative: bool = False) -> SequenceInstance:
    def gen():
        is_negative = is_start_negative
        for val in sequence.values:
            yield val * -1 if is_negative else val
            is_negative = not is_negative
    return SequenceInstance(gen(), *sequence.comments, f"With alternating sign; start {'negative' if is_start_negative else 'positive'}")


# ======== TARGETS ======== #
# Sequences that need to be generated
sequences: Final[list[SequenceInstance]] = [
    seq_constant(0),
    seq_linear(start=0, shift=10),
    seq_linear(start=20, shift=-2.2),
    seq_mult(start=2, mult=2),
    seq_mult(start=-1000, mult=-0.75),
    seq_power(2),
    seq_lucas(0, 1),
    seq_lucas(2, 1),
    seq_mod_alt_sign(seq_constant(1), is_start_negative=True),
    seq_mod_alt_sign(seq_linear(start=5, shift=2))
]


# ======== GENERATION ======== #
def main():

    # Generate sequences
    print("Generating sequences...")
    output_strings = list()

    for i, sequence in enumerate(sequences):
        # Take rounding and length into account
        values = map(lambda x: round(x, round_decimals), islice(sequence.values, sequence_length))
        string_values = map(str, values)
        # Format sequence elements
        sequence_string = sequence_format.format(sequence=element_separator.join(string_values), index=i)
        # Format comments
        comments_string = comment_separator.join(map(lambda s: comment_format.format(text=s), sequence.comments))
        # Concat for output
        output_strings.append(f"{comments_string}{separator_between_comment_and_sequence}{sequence_string}")

    output_payload = output_format.format(sequences=sequence_separator.join(output_strings))

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
