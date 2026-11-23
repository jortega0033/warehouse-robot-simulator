"""Command line entry point: `python -m warehouse_sim <command>`."""

import argparse
import sys

from . import __version__

NOT_IMPLEMENTED_EXIT = 3


def build_parser():
    parser = argparse.ArgumentParser(prog="python -m warehouse_sim", description="Offline warehouse robot simulator.")
    parser.add_argument("--version", action="version", version=f"warehouse_sim {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="run a scenario and write a replay")
    run.add_argument("scenario")
    run.add_argument("--out", required=True)
    run.set_defaults(ticket="WH-01a (sub-issue of #2)")

    serve = sub.add_parser("serve", help="run a scenario and open the local browser view")
    serve.add_argument("scenario", nargs="?", default="scenarios/single-order.json")
    serve.add_argument("--port", type=int, default=8780)
    serve.add_argument("--no-open", action="store_true")
    serve.set_defaults(ticket="WH-01b (sub-issue of #2)")

    validate = sub.add_parser("validate", help="validate a scenario against the schema and caps (exit 0 valid, 2 invalid)")
    validate.add_argument("scenario")
    validate.set_defaults(ticket="WH-07 (#10)")

    compare = sub.add_parser("compare", help="compare two assignment policies on a seeded workload")
    compare.add_argument("--seed", type=int, required=True)
    compare.set_defaults(ticket="#6 (WH-05)")

    scale = sub.add_parser("scale", help="run the scale report")
    scale.set_defaults(ticket="#7 (WH-06)")
    return parser


def main(argv=None):
    args, _ = build_parser().parse_known_args(argv)
    print(f"not implemented yet: see {args.ticket}", file=sys.stderr)
    return NOT_IMPLEMENTED_EXIT


if __name__ == "__main__":
    sys.exit(main())
