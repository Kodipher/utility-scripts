# utility-scripts

[![GitHub Licence Badge](https://img.shields.io/github/license/Kodipher/utility-scripts)](https://github.com/Kodipher/utility-scripts/blob/main/LICENSE)

A collection of niche standalone python scripts (and also some code that can be imported).

All standalone scripts can be found in the `scripts` directory. Each script has an outlined problem as the first comment, followed by constants that work as settings. 

Scripts that are designed to be used as imports can be found in the `imports` directory.

### Standalone scripts:

| Script                       | Task                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| `durations_set_searcher.py`  | Finds sets of pools and durations of actions, so that a random selection of a pool is balanced. |
| `sequence_generator.py`      | Generates sequences of numbers.                              |
| `ktane_repo_filter_maker.py` | For playing KTaNE. Using a no modded module profile, generates a filter for the experts to use on the manual repository. |
| `color_tokki_svg_generator.py` | Generates an svg image using ColorTokki constructed script ([see on Omniglot](https://www.omniglot.com/conscripts/colorhoney.php)) with some adjustments to allow punctuation and spaces without breaking the flow of the script. |

### Imports:

| Import              | Functionality                                                |
| ------------------- | ------------------------------------------------------------ |
| `matrix_file_io.py` | Provides a very basic way to read and write 2d numpy arrays. |

