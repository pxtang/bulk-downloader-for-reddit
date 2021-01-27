import argparse
import subprocess
from os import scandir
from time import sleep


def parse():
    """Initialize argparse and add arguments"""

    parser = argparse.ArgumentParser(allow_abbrev=False,
                                     description="This program batch downloads " \
                                                 "media from reddit posts")
    parser.add_argument("--directory", "-d",
                        help="Specifies the directory where post directories have been " \
                             "downloaded to previously",
                        metavar="DIRECTORY", required=True)

    parser.add_argument("--limit", "-l",
                        default=150,
                        help="default: 150",
                        metavar="Limit",
                        type=int)

    parser.add_argument("--start",
                        help="Specify directory to start grabbing from. Soft comparison match - lowercase only",
                        metavar="DIRECTORY",
                        default="")

    parser.add_argument("--end",
                        help="Specify directory to stop grabbing at. Soft comparison match - lowercase only",
                        metavar="DIRECTORY",
                        default="")

    parser.add_argument("--quit", "-q",
                        help="Auto quit after each process finishes",
                        action="store_true",
                        default=False)

    return parser.parse_args()


def start_dl(dir, name, limit, quit):
    command = f"python3 ./script.py  --submitted --sort new --time all --limit {limit} --no-dupes " \
                   f"--directory '{dir}{name}' --user '{name}'"
    if quit:
        command += " --quit"
    print(f"Command being executed:\n`{command}`"
          "\n----------")
    subprocess.run(command, shell=True)

    if quit:
        print("Sleeping 10 seconds before automatically moving on")
        sleep(10)


def load_exclusions():
    exclusions = set()
    with open("exclusions.txt", "r") as file_in:
        text = file_in.read()
        exclusions = set(text.split("\n"))
    return exclusions


def main(args):
    # get exclusion dirs
    exclusions = load_exclusions()
    main_dir = args.directory
    if main_dir[-1] != "/":
        main_dir += "/"
    with scandir(main_dir) as sc:
        for dir in sc:
            if not dir.is_dir():
                continue
            if args.start != "" and args.start > dir.name.lower():
                continue
            if args.end != "" and args.end < dir.name.lower():
                print(f"Directory {dir.name} is after {args.end}, stopping.")
                break
            if dir.name in exclusions:
                continue
            start_dl(main_dir, dir.name, args.limit, args.quit)


if __name__ == '__main__':
    args = parse()
    main(args)
