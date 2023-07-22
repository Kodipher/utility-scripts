from __future__ import annotations
from typing import Final, Sequence, Iterable

import math
import itertools
from traceback import format_exc


# ======== SEARCH SETTINGS ======== #
durations_range: Final[tuple[int, int]] = (4, 25)   # All possible non-forced durations

durations_min_diff: Final[int] = 2                  # Min and max differences between durations in a set
durations_min_mult: Final[float] = 1.5
durations_max_mult: Final[float] = 4.0

duration_set_size_range: Final[tuple[int, int]] = (3, 20)           # Number of durations in a set
duration_set_forced_first_added: Final[Sequence[int]] = [1, 2]      # Lowest durations that must be present in all sets

stage_count_range: Final[tuple[int, int]] = (4, 4)          # Number of durations in a pool
pool_target_sum_range: Final[tuple[int, int]] = (3, 20)     # Acceptable range of total durations
min_pools_with_the_same_sum: Final[int] = 3                 # Number of pools with the same sum to form valid pool list



# ======== UTILS ======== #
def range_inclusive(start: int, end: int, step: int = 1) -> Iterable[int]:
    return range(start, end + 1, step)

def range_inclusive_tuple(tuple_range: tuple[int, int] | tuple[int, int, int]) -> Iterable[int]:
    return range_inclusive(*tuple_range)

def in_range_inclusive_tuple(value: float, tuple_range: tuple[float, float]) -> bool:
    return value >= tuple_range[0] and value <= tuple_range[1]


# ======== SEARCHER ======== #
def generate_sets() -> Iterable[Sequence[int]]:
    """Generates duration sets in accordance with settings. All sets have durations sorted from low to high."""

    for set_size in range_inclusive_tuple(duration_set_size_range):

        generate_target_count = set_size - len(duration_set_forced_first_added)

        if generate_target_count < 0:
            continue

        if generate_target_count == 0:
            yield tuple(sorted(duration_set_forced_first_added))
            continue

        def generate_next_durations_with_append(current_seq: Sequence[int], append_count: int) -> Iterable[Sequence[int]]:
            """
            Given current sequence, return all possible sequences with appended next element.
            Perform appending recursively until the target length is reached.
            """

            # Generation finished for branch
            if append_count <= 0:
                yield current_seq
                return

            # Find next starting duration
            durations_range_start, durations_range_end = durations_range

            current_seq_len = len(current_seq)
            if current_seq_len > 0:

                last_elem = current_seq[current_seq_len - 1]

                # Set start bounds in relation to last element
                durations_range_start = max(
                    durations_range_start,
                    last_elem + durations_min_diff,
                    math.floor(last_elem * durations_min_mult)
                )

                # Set end bounds in relation to last element
                durations_range_end = min(
                    durations_range_end,
                    math.ceil(last_elem * durations_max_mult)
                )

            # If impossible to complete sequence, return nothing: failed branch
            if durations_range_start > durations_range_end:
                return

            # Generate all next branches
            for next_duration in range_inclusive(durations_range_start, durations_range_end):
                seq_with_append = tuple(current_seq) + (next_duration,)
                yield from generate_next_durations_with_append(seq_with_append, append_count - 1)
            
        sorted_forced = tuple(sorted(duration_set_forced_first_added))
        yield from generate_next_durations_with_append(sorted_forced, generate_target_count)


def generate_pools(durations_set: Sequence[int], stage_count: int) -> dict[int, list[Sequence[int]]]:
    """
    Generates all possible pools from durations sets, in according to the settings.
    Stage count is provided as an argument.
    Returns filtered pools grouped by their sum.
    """

    # Generate all possible pools
    all_pools = itertools.combinations_with_replacement(durations_set, stage_count)
    pool: Sequence[int]

    # Sort pools by duration
    pools_by_total_duration: dict[int, list[Sequence[int]]] = dict()

    for pool in all_pools:

        total_duration = sum(pool)

        if total_duration not in pools_by_total_duration.keys():
            pools_by_total_duration[total_duration] = [pool]
        else:
            pools_by_total_duration[total_duration].append(pool)

    # Filter pools
    pools_filtered: dict[int, list[Sequence[int]]] = dict()
    for total_duration, pool_list in pools_by_total_duration.items():

        # Filter by sum being too high or low
        if not in_range_inclusive_tuple(total_duration, pool_target_sum_range):
            continue

        # Filter by pool count
        if len(pool_list) < min_pools_with_the_same_sum:
            continue

        # Filter by all durations being present
        durations_used_set = set()
        for pool in pool_list:
            for duration in pool:
                durations_used_set.add(duration)

        if durations_used_set != set(durations_set):
            continue

        # Checks passed
        pools_filtered[total_duration] = pool_list
        
    return pools_filtered


def print_pools(stage_count: int, durations_set: Sequence[int], pools_by_sum: dict[int, list[Sequence[int]]]):
    print()
    print(f"Stage count: {stage_count}")
    print(f"Set: {durations_set}")
    for total_duration, pool_list in pools_by_sum.items():
        print(f"Pools (sum {total_duration}): {pool_list}")


def main():

    # Generate durations sets
    print(f"Generating durations sets...")
    durations_sets = list(generate_sets())
    print(f"Found {len(durations_sets)} durations sets...")

    # Generate durations pools
    print(f"Generating and filtering pools...")
    for stage_count in range_inclusive_tuple(stage_count_range):
        for durations_set in durations_sets:
            pools = generate_pools(durations_set, stage_count)
            if len(pools) != 0:
                print_pools(stage_count, durations_set, pools)


if __name__ == "__main__":
    try:
        main()
        input("Press enter to exit")
    except Exception:
        print("An error has occurred:")
        print(format_exc())
        input("Press enter to exit")
