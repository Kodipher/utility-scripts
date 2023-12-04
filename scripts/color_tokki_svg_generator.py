from __future__ import annotations
from typing import Final

from pathlib import Path
from textwrap import wrap
from itertools import chain
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
# The height of line separation, compared to the size of one glyph
line_separation_height: Final[float] = 0.4

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
def character_position_to_block_position(
        line_index: int,
        column_index: int
    ) -> (float, float, bool): # pair_x_abs, pair_y_abs, is vertical

    # Calculate block position (group of 4)
    # all positions are in rectangle widths
    block_x = column_index // 4
    block_y = line_index
    position_within_block = column_index % 4

    pair_x_absolute = block_x * 2
    pair_y_absolute = block_y * 2 + line_separation_height * line_index

    if position_within_block > 1:
        pair_x_absolute += 1
    
    if position_within_block % 2 == 1:
        pair_y_absolute += 1

    is_vertical = position_within_block == 1 or position_within_block == 2

    return (pair_x_absolute, pair_y_absolute, is_vertical)


def create_rectangle(x, y, width, height, color: str | (str, str)):
    if isinstance(color, str):
        return rect_template.format(x=x, y=y, width=width, height=height, color=color)
    else:
        return rect_outline_template.format(x=x, y=y, width=width, height=height, fill_color=color[0], outline_color=color[1])


def create_rectangle_pair(
        line_index: int,
        column_index: int, # index in that line
        top_color: str | (str, str),
        bottom_color: str | (str, str)
    ) -> (str, str):

    pair_data = (dict(), dict())

    # Create rectangles with relative positioning
    pair_data[0]["x"] = 0
    pair_data[1]["x"] = pair_data[0]["x"]
    pair_data[0]["y"] = rectangle_first_offset_in_widths * glyph_size
    pair_data[1]["y"] = rectangle_second_offset_in_widths * glyph_size
    pair_data[0]["width"] = glyph_size
    pair_data[1]["width"] = pair_data[0]["width"]
    pair_data[0]["height"] = rectangle_height_in_widths * glyph_size
    pair_data[1]["height"] = pair_data[0]["height"]

    # Offset to absolute positions and rotate the pair
    x_offset, y_offset, is_vertical = character_position_to_block_position(line_index, column_index)

    if is_vertical:
        for i in range(2):
            pair_data[i]["x"], pair_data[i]["y"] = pair_data[i]["y"], pair_data[i]["x"]
            pair_data[i]["width"], pair_data[i]["height"] = pair_data[i]["height"], pair_data[i]["width"]

    pair_data[0]["x"] += x_offset * glyph_size
    pair_data[1]["x"] += x_offset * glyph_size
    pair_data[0]["y"] += y_offset * glyph_size
    pair_data[1]["y"] += y_offset * glyph_size

    # Create and return
    return (
        create_rectangle(**pair_data[0], color=top_color),
        create_rectangle(**pair_data[1], color=bottom_color)
    )


def main():

    # Read input file
    print("Reading input file...")
    input_file_path = Path(input_file)
    if not (input_file_path.exists() and input_file_path.is_file()):
        print(f"File \"{input_file}\" does not exist or is not a file.")
        return

    text = input_file_path.read_text()
    text_lines = list(
        chain.from_iterable(
            map(
                    lambda s: wrap(s, width=image_width*2, replace_whitespace=False),
                    text.splitlines()
                )
            )
        )

    # Generate image
    print("Generating image...")

    rectangles: list[str] = list()  # I wish i could preallocate certain length

    for line_index, line in enumerate(text_lines):

        col_index = 0

        for character in line:

            color_pair = alphabet.get(character, None)

            if color_pair is None:
                print(f"Character {repr(character)} at row {line_index+1} col {col_index+1} is not defined in the alphabet. Skipping.")
                continue

            top_color = color_palette[color_pair[0]]
            bottom_color = color_palette[color_pair[1]]

            rectangles.extend(create_rectangle_pair(line_index, col_index, top_color, bottom_color))
            col_index += 1

    image = svg_template.format(
        width=image_width*glyph_size,
        height=len(text_lines)*2*glyph_size,
        content="\n".join(rectangles)
    )

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
