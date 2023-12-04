from __future__ import annotations
from typing import Final, Sequence, Iterable

import math
from pathlib import Path
from traceback import format_exc


# == PROBLEM ==
# Given a string of text, generate an svg image with
# that text written using ColorTokki constructed script.
#
# Script info on Omniglot: https://www.omniglot.com/conscripts/colorhoney.php 


# ======== SETTINGS ======== #
# Filename to write resulting image into
output_file: Final[str] = "generated_image.svg"
# TODO: Add all other settings


# ======== DOCUMENT TEMPLATES ======== #
# TODO


# ======== GENERATION ======== #
def main():

    # Generate sequences
    print("Generating image...")
    image = ""
    # TODO: Generate image

    # Write to file
    print("Writing output...")
    bytes_written = Path(output_file).write_text(image)
    print(f"{bytes_written} bytes written to \"{output_file}\"")


if __name__ == "__main__":
    try:
        main()
        input("Press enter to exit")
    except Exception:
        print("An error has occurred:")
        print(format_exc())
        input("Press enter to exit")
