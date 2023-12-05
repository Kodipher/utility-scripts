from __future__ import annotations
from typing import Final, Iterable, Callable, Any, TypeVar

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
# Some alterations have been made
# and are available via extended alphabet:
# Black and white solid glyphs are spaces, line breaks and punctuation;
# Black and white glyphs with one outline glyph are brackets;
# Colored glyphs with top bar outlines are digits;
# Colored glyphs with bottom bar outlined are misc symbols.


# ======== SETTINGS ======== #
# Path to the file with text to spell out
input_file: Final[str] = "script.txt"
# Filename to write resulting image into.
# Supports {name} for input file name without extension.
output_file: Final[str] = "{name}.generated.svg"

# The width of one horizontal rectangle in em.
# A glyph takes 1 width by 1 width rectangle space and has no padding.
# Basis for all sizes and positioning.
glyph_size: Final[int] = 14
# Width of the image in the number of characters
image_width: Final[int] = 32
# The height of line separation, compared to the size of one glyph.
# Only applies if line breaks are not treated as a glyph.
line_separation_height: Final[float] = 0.4
# Outline width, in em. The outline is fully inside the rectangle
outline_size: Final[float] = 0.5

# Wether to place a default glyph in place of unknown characters (True) or skip them completely (False)
keep_unknown_characters: Final[bool] = True
# Wether to use extended alphabet
use_extended_alphabet: Final[bool] = True
# Wether to use space as a glyph (False) or change spaces to line breaks (True).
# Requires extended alphabet to have an effect, otherwise True.
spaces_become_line_breaks: Final[bool] = True
# Wether to keep the line breaks inline as glyphs.
# Requires extended alphabet to have an effect, otherwise False.
inline_line_breaks: Final[bool] = False


# ======== ALPHABET ======== #
# The color palette of svg (css) colors.
# Each color is assigned a key to be used by glyphs in the alphabet.
# A tuple of 2 colors can be given, then the first color is the fill and the second is outline.
color_palette: Final[dict[str, str | (str, str)]] = {

    # Default colors
    "R": "#FF0000", # Red
    "G": "#19A319", # Green
    "B": "#0167FF", # dark Blue
    "S": "#00CCFF", # Sky blue
    "V": "#CC66FF", # Violet
    "Y": "#FFCE0C", # Yellow

    # Black and white
    "BW0": "#333333",
    "BW1": "#666666",
    "BW2": "#999999",
    "BW3": "#CCCCCC",

    # Colors but outline only
    "oR": ("#FFFFFF00", "#FF0000"), 
    "oG": ("#FFFFFF00", "#19A319"), 
    "oB": ("#FFFFFF00", "#0167FF"), 
    "oS": ("#FFFFFF00", "#00CCFF"), 
    "oV": ("#FFFFFF00", "#CC66FF"), 
    "oY": ("#FFFFFF00", "#FFCE0C"),
    "oBW1": ("#FFFFFF00", "#666666"),
    "oBW3": ("#FFFFFF00", "#CCCCCC"),
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
}
# Same as alphabet but only the extended characters
alphabet_extension: Final[dict[str, (str, str)]] = {

    # Punctuation
    # 0 -- dark, 3 -- light
    # y -- bottom, x -- top, i.e. (x,y)
    #
    # 3 "'*s
    # 2 &-:n
    # 1  /; 
    # 0 !?,.
    #   0123
    ' ': ("BW3", "BW3"),
    '\n':("BW3", "BW2"),
    '.': ("BW3", "BW0"),
    ',': ("BW2", "BW0"),
    '?': ("BW1", "BW0"),
    '!': ("BW0", "BW0"),
    '-': ("BW1", "BW2"),
    '&': ("BW0", "BW2"),
    ';': ("BW2", "BW1"),
    ':': ("BW2", "BW2"),
    '*': ("BW2", "BW3"),
    '\'':("BW1", "BW3"),
    '\"':("BW0", "BW3"),
    '/': ("BW1", "BW1"),
    '\\':("BW1", "BW1"), # same as '/'

    # Brackets
    # outline on the inside
    # from dark to light: [<{(
    '[': ("BW0", "oBW1"),
    '<': ("BW1", "oBW1"),
    '{': ("BW2", "oBW1"),
    '(': ("BW3", "oBW1"),
    ']': ("oBW1", "BW0"),
    '>': ("oBW1", "BW1"),
    '}': ("oBW1", "BW2"),
    ')': ("oBW1", "BW3"),

    # Digits
    # Equivalent to letter positions 0=26, 1, .. 9
    # but with outline on the top
    '0': ("oS", "B"), # Z
    '1': ("oV", "V"), # A
    '2': ("oV", "S"), # B
    '3': ("oV", "B"), # C
    '4': ("oV", "G"), # D
    '5': ("oR", "R"), # E
    '6': ("oR", "G"), # F
    '7': ("oR", "B"), # G
    '8': ("oR", "S"), # H
    '9': ("oG", "G"), # I
    
    # Misc signs
    # Equivalent to respective letters but outline on the bottom
    '#': ("G", "oR"), # N for Number
    '№': ("G", "oR"), # same as '#'
    '%': ("V", "oB"), # C for per Cent
    '^': ("R", "oR"), # E for Exponent
    '=': ("Y", "oS"), # Q for eQuality
    '+': ("V", "oV")  # A for Addition
}
# The color keys for the unknown glyph
glyph_unknown: Final[(str, str)] = ("oBW3", "oBW3")


# ======== ELEMENTS AND MEASUREMENTS ======== #
svg_template: Final[str] = """
<svg version="1.1"
     width="{width}em" height="{height}em"
     xmlns="http://www.w3.org/2000/svg">
{content}
</svg>
"""
rect_template: Final[str] = """<rect x="{x}em" y="{y}em" width="{width}em" height="{height}em" fill="{color}" />"""
rect_outline_template: Final[str] = """<rect x="{x}em" y="{y}em" width="{width}em" height="{height}em" fill="{fill_color}" stroke="{outline_color}" stroke-width="{outline_width}" />"""

# Measurements (based on pixel measurements)
# Each glyph takes 1 width by 1 width square
# Assume squares have no padding
rectangle_height_in_widths: Final[float] = 14.0/47
rectangle_same_glyph_distance_in_widths: Final[float] = 5.0/47
rectangle_first_offset_in_widths: Final[float] = 0.5 - rectangle_same_glyph_distance_in_widths / 2 - rectangle_height_in_widths
rectangle_second_offset_in_widths: Final[float] = rectangle_first_offset_in_widths + rectangle_height_in_widths + rectangle_same_glyph_distance_in_widths


# ======== UTILS AND GENERATION ======== #
T = TypeVar("T")
U = TypeVar("U")
def select_many(delegate: Callable[[T], Iterable[U]], iterable: Iterable[T]) -> Iterable[U]:
    return chain.from_iterable(map(delegate, iterable))
    

def find_rectangle_position(
        line_index: int,
        column_index: int
    ) -> (float, float, bool): # pair_x_abs, pair_y_abs, is_vertical

    # Calculate block position (group of 4)
    # all positions are in rectangle widths
    block_x = column_index // 4
    block_y = line_index
    position_within_block = column_index % 4

    # Based on block position calculate the pair position
    pair_x_absolute: float = block_x * 2
    pair_y_absolute: float = block_y * 2

    if position_within_block > 1:
        pair_x_absolute += 1
    
    if position_within_block % 2 == 1:
        pair_y_absolute += 1

    if pair_x_absolute >= image_width:
        print(f"Character at wrapped row {line_index+1} col {column_index+1} is out of bound of {image_width} characters width area")

    is_vertical = position_within_block == 1 or position_within_block == 2

    # Add line separation if line breaks are not inlined
    if not use_extended_alphabet or not inline_line_breaks:
        pair_y_absolute += line_separation_height * line_index

    # Return
    return (pair_x_absolute, pair_y_absolute, is_vertical)


def create_rectangle(x, y, width, height, color: str | (str, str)):
    if isinstance(color, str):
        return rect_template.format(x=x, y=y, width=width, height=height, color=color)
    else:
        # Keep outline inside the rectangle
        x += outline_size/2
        y += outline_size/2
        width -= outline_size
        height -= outline_size
        # Crate the rectangle
        return rect_outline_template.format(x=x, y=y, width=width, height=height, fill_color=color[0], outline_color=color[1], outline_width=outline_size)


def generate_rectangle_pair(
        line_index: int,
        column_index: int,
        top_color: str | (str, str),
        bottom_color: str | (str, str)
    ) -> (str, str):

    pair_data: (dict[str, Any], dict[str, Any]) = (dict(), dict())

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
    x_offset, y_offset, is_vertical = find_rectangle_position(line_index, column_index)

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

    # Check some settings
    if image_width < 1:
        print("Image width must be at least 1 characters. Aborting.")
        return
    
    # Read input file
    print("Reading input file...")
    input_file_path = Path(input_file)
    if not (input_file_path.exists() and input_file_path.is_file()):
        print(f"File \"{input_file}\" does not exist or is not a file.")
        return

    text = input_file_path.read_text()

    # Splitting into lines
    print("Splitting into lines according to chosen settings...")
    text_lines: list[str]

    if use_extended_alphabet:

        if inline_line_breaks:

            # First normalize line breaks to all be "\n"
            text = "\n".join(text.splitlines())

            # Replace spaces if needed
            if spaces_become_line_breaks:
                text.replace(' ', '\n')

            # Batch by how many characters fit
            batching_width = image_width * 2
            text_lines = [text[i:i+batching_width] for i in range(0, len(text), batching_width)]
       
        else:
            
            # First split by new lines
            text_lines = text.splitlines()

            # Then split by spaces
            if spaces_become_line_breaks:
                text_lines = list(select_many(lambda line: line.split('\n'), text_lines))

            # Then wrap it around but keep empty lines
            text_lines = list(select_many(
                lambda s: ("",) if len(s.strip()) == 0 else wrap(s, width=image_width*2, replace_whitespace=False),
                text_lines
            ))
        
    else:
        
        # Split on new lines,
        # then split each line on space
        text_lines = list(select_many(
            lambda line: line.split(' '),
            text.splitlines()
        ))
    

    # Generate image
    print("Generating image...")
    rectangles: list[str] = list()  # I wish i could preallocate certain length

    for line_index, line in enumerate(text_lines):

        col_index = 0
        for character in line.upper():
            
            # Find colors
            color_pair = alphabet.get(character, None)

            if use_extended_alphabet and color_pair is None:
                color_pair = alphabet_extension.get(character, None)

            if color_pair is None:
                print(f"Character {repr(character)} at wrapped row {line_index+1} col {col_index+1} is not defined in the alphabet. Skipping.")
                
                if keep_unknown_characters:
                    color_pair = glyph_unknown
                else:
                    continue

            # Create and add the rectangle
            top_color = color_palette[color_pair[0]]
            bottom_color = color_palette[color_pair[1]]
            rectangles.extend(generate_rectangle_pair(line_index, col_index, top_color, bottom_color))

            # Move to the next column in the resulting image
            col_index += 1

    # Create the image
    image_height: float = len(text_lines) * (2 * glyph_size)

    if not use_extended_alphabet or not inline_line_breaks:
        image_height += len(text_lines) * line_separation_height

    image = svg_template.format(
        width=image_width*glyph_size,
        height=image_height,
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
