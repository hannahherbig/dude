from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path

from humanize import naturalsize
from tabulate import tabulate


def walk(top: Path, sizes=None):
    if sizes is None:
        sizes = defaultdict(int)
    try:
        size = top.lstat().st_size
        sizes[top] += size
        for parent in top.parents:
            sizes[parent] += size
        if top.is_dir():
            for child in top.iterdir():
                walk(child, sizes)
    except FileNotFoundError:  # pragma: no cover
        pass
    return sizes


def main():
    parser = ArgumentParser()
    parser.add_argument("top", type=Path, nargs="?", default=Path("."))
    parser.add_argument("-f", "--tablefmt", default="plain")
    args = parser.parse_args()

    sizes = walk(args.top)
    table = []
    for path, size in sorted(sizes.items(), key=lambda v: (v[1], v[0])):
        if args.top in path.parents or args.top == path:
            end = "/" if path.is_dir() and not path.as_posix().endswith("/") else ""
            table.append(
                (*naturalsize(size, binary=True).split(), path.as_posix() + end)
            )

    print(tabulate(table, tablefmt=args.tablefmt))


if __name__ == "__main__":
    main()
