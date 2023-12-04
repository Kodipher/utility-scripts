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
#
# Some alterations have been made to allow for spaces and
# punctuation without breaking the flow of writing.


# ======== SETTINGS ======== #
# Path to the file with text to spell out
input_file: Final[str] = "script.txt"
# Filename to write resulting image into.
# Supports {name} for input file name without extension.
output_file: Final[str] = "{name}.generated.svg"

# The width of one horizontal rectangle excluding padding in pt.
# Basis for all sizes and positioning.
glyph_size: Final[int] = 10
# Width of the image in the number of characters
image_width: Final[int] = 10

# The background color of the resulting image
background_color: Final[str] = "white"
# The color palette of svg (css) colors.
# Each color is assigned a key to be used by glyphs in the alphabet.
# A tuple of 2 colors can be given, then the first color is the fill and the second is outline.
color_palette: Final[dict[str, str | (str, str)]] = {
    "R": "#FF0000", # Red
    "G": "#19A319", # Green
    "B": "#0167FF", # dark Blue
    "S": "#00CCFF", # Sky blue
    "V": "#CC66FF", # Violet
    "Y": "#FFCE0C", # Yellow

    "GA": "#7F7F7F", # Average Gray
    "GB": "#303030", # darker (Blacker) Gray
    "GW": ("#D1D1D1", "#303030"), # lighter (Whiter) Gray
}
# The color keys used for each letter in order of top, then bottom (light then dark)
alphabet: Final[dict[str, (str, str)]] = {

    # Vowels
    'A': ("V", "V"),
    'E': ("R", "R"),
    'I': ("G", "G"),
    'O': ("Y", "Y"),
    'U': ("B", "B"),
    'Y': ("S", "S"),

    # Consonants
    'B': ("V", "S"),
    'C': ("V", "B"),
    'D': ("V", "G"),
    'F': ("R", "G"),
    'G': ("R", "B"),
    'H': ("R", "S"),
    'J': ("G", "B"),
    'K': ("G", "S"),
    'L': ("G", "V"),
    'M': ("G", "Y"),
    'N': ("G", "R"),
    'P': ("Y", "V"),
    'Q': ("Y", "S"),
    'R': ("Y", "B"),
    'S': ("Y", "G"),
    'T': ("Y", "R"),
    'V': ("B", "S"),
    'W': ("B", "V"),
    'X': ("B", "Y"),
    'Z': ("S", "B"),

    # Extended
    ' ': ("GW", "GW"),
    '.': ("GW", "GB"),
    "?": ("GA", "GB"),
    '!': ("GB", "GB"),
    '-': ("GA", "GA"),
    ',': ("GW", "GA"),
    "\"":("GA", "GW"),
    "\'":("GA", "GW")
    
}


# ======== ELEMENTS AND MEASUREMENTS ======== #
svg_template: Final[str] = """
<svg version="1.1"
     width="{width}pt" height="{height}pt"
     xmlns="http://www.w3.org/2000/svg">
{content}
</svg>
"""
rect_template: Final[str] = "<rect x=\"{x}\" y=\"{y}\" width=\"{width}\" height=\"{height}\" fill=\"{color}\" />"
rect_outline_template: Final[str] = "<rect x=\"{x}\" y=\"{y}\" width=\"{width}\" height=\"{height}\" fill=\"{fill_color}\" stoke=\"{outline_color}\" />"

# Measurements (based on pixel measurements)
# Each glyph takes 1 width by 1 width square
# Assume squares have no padding
rectangle_height_in_widths: Final[float] = 14.0/47
rectangle_same_glyph_distance_in_widths: Final[float] = 5.0/47
rectangle_first_offset_in_widths: Final[float] = 0.5 - rectangle_same_glyph_distance_in_widths / 2 - rectangle_height_in_widths
rectangle_second_offset_in_widths: Final[float] = rectangle_first_offset_in_widths + rectangle_height_in_widths + rectangle_same_glyph_distance_in_widths


# ======== GENERATION ======== #
def main():

    # Read input file
    print("Reading input file...")
    input_file_path = Path(input_file)
    if not (input_file_path.exists() and input_file_path.is_file()):
        print(f"File \"{input_file}\" does not exist or is not a file.")
        return

    text = input_file_path.read_text()

    # Generate image
    print("Generating image...")
    image = ""
    # TODO: Generate image

    # Write to file
    print("Writing output...")
    output_file_path = Path(output_file.format(name=input_file_path.stem))
    bytes_written = output_file_path.write_text(image)
    print(f"{bytes_written} bytes written to \"{output_file_path}\"")


if __name__ == "__main__":
    try:
        main()
        input("Press enter to exit")
    except Exception:
        print("An error has occurred:")
        print(format_exc())
        input("Press enter to exit")
