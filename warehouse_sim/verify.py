"""Independent replay checker. Must not import engine or scheduler; it applies its own rules."""

import argparse
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m warehouse_sim.verify",
        description="Verify a replay independently (exit 0 accepted, 1 rejected with the first invalid tick).",
    )
    parser.add_argument("replay", help="path to a replay JSON file")
    parser.parse_args(argv)
    print("not implemented yet: see #3 (WH-02)", file=sys.stderr)
    return 3


if __name__ == "__main__":
    sys.exit(main())
