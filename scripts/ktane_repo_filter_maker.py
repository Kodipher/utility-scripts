from __future__ import annotations
from typing import Final

import json
from datetime import date
from pathlib import Path
from traceback import format_exc


# == PROBLEM ==
# In context of the game Keep Talking and Nobody Explodes
# and the Repository of Manual Pages at https://ktane.timwi.de
#
# Given a defuser profile with all modded modules disabled,
# create an expert profile that
# - includes all of the modules enabled
# - includes all vanilla modules
# - has date of creation in the file name
#


# ======== SETTINGS ======== #
# Path to no modded modules profile
no_modded_modules_filter_location: Final[str] = "../_No Modded Modules.json"
# Format of the output file. Supports {date} for current date
output_name_location_format: Final[str] = "ManualRepoFilter - {date}.json"
# Format of the date used for {date} above
date_format: Final[str] = "%d-%b-%Y"
# List of vanilla modules (appended to the filter regardless of no modded profile)
vanilla_modules: Final[list[str]] = [
    "BigButton",
    "Venn",
    "Keypad",
    "Maze",
    "Memory",
    "Morse",
    "Password",
    "Simon",
    "WhosOnFirst",
    "Wires",
    "WireSequence"
]


def main():
    
    no_modded_path = Path(no_modded_modules_filter_location)
    if not (no_modded_path.exists() and no_modded_path.is_file()):
        print(f"File \"{no_modded_modules_filter_location}\" does not exist or is not a file.")
        return

    print("Reading no modded modules profile...")
    no_modded_profile = json.loads(no_modded_path.read_text())

    print("Forming a filter profile...")
    module_list = list(no_modded_profile["DisabledList"])
    module_list.extend(vanilla_modules)

    filter_profile = {
        "DisabledList": [],
        "EnabledList": module_list,
        "Operation": 0
    }
    filter_profile_string = json.dumps(filter_profile, indent=2)

    # Write final file
    print("Writing to output file...")
    current_date_string = date.today().strftime(date_format)
    output_path = Path(output_name_location_format.format(date=current_date_string))
    bytes_written = output_path.write_text(filter_profile_string)
    print(f"{bytes_written} bytes written.")


if __name__ == "__main__":
    try:
        main()
        input("Press enter to exit")
    except Exception:
        print("An error has occurred:")
        print(format_exc())
        input("Press enter to exit")
