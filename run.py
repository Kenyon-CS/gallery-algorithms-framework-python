from __future__ import annotations

import sys

from gallery.algorithm import create_algorithm
from gallery.evaluator import Evaluator
from gallery.models import ScoringConfig
from gallery.parser import load_gallery, load_scoring, load_show


def print_usage() -> None:
    print(
        "Usage:\n"
        "  python3 run.py <gallery.yaml> <show.yaml> <algorithm> [scoring.yaml]\n\n"
        "Algorithms:\n"
        "  greedy\n"
        "  random"
    )


def main(argv: list[str]) -> int:
    try:
        if len(argv) < 4 or len(argv) > 5:
            print_usage()
            return 1

        gallery_path = argv[1]
        show_path = argv[2]
        algorithm_name = argv[3]

        gallery = load_gallery(gallery_path)
        show = load_show(show_path)
        scoring = load_scoring(argv[4]) if len(argv) == 5 else ScoringConfig()

        evaluator = Evaluator(scoring)
        algorithm = create_algorithm(algorithm_name)
        result = algorithm.solve(gallery, show, evaluator)

        print("Gallery Planner")
        print("===============")
        print(f"Gallery:   {gallery.name}")
        print(f"Show:      {show.title}")
        print(f"Algorithm: {result.algorithm_name}")
        print()

        print("Score Breakdown")
        print("---------------")
        print(f"Compatibility:   {result.breakdown.compatibility:.2f}")
        print(f"Capacity:        {result.breakdown.capacity:.2f}")
        print(f"Lighting:        {result.breakdown.light:.2f}")
        print(f"Room Preference: {result.breakdown.room_preference:.2f}")
        print(f"Unplaced:        {result.breakdown.unplaced:.2f}")
        print(f"Duplicate Use:   {result.breakdown.duplicate_use:.2f}")
        print(f"TOTAL:           {result.score:.2f}")
        print()

        print("Placements")
        print("----------")
        for index, art in enumerate(show.artworks):
            zone_index = result.placement[index]
            if zone_index < 0:
                print(f"{art.id} ({art.title}) -> UNPLACED")
            else:
                zone = gallery.zones[zone_index]
                print(
                    f"{art.id} ({art.title}) -> {zone.id} "
                    f"[room={zone.room}, type={zone.type.value}, cap={zone.capacity}]"
                )

        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
