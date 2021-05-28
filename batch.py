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

    parser.add_argument("--limit", "-L",
                        default=150,
                        help="default: 150",
                        metavar="Limit",
                        type=int)

    parser.add_argument("--start",
                        help="Specify letter to start grabbing from. Soft comparison match - lowercase only. Inclusive.",
                        metavar="DIRECTORY",
                        default="")

    parser.add_argument("--end",
                        help="Specify letter to stop grabbing at. Soft comparison match - lowercase only. Exclusive.",
                        metavar="DIRECTORY",
                        default="")

    parser.add_argument("--users", "-u",
                        help="Comma separated list of users")

    return parser.parse_args()


def start_dl(directory, name, limit):
    command = f"python3.9 -m bdfr download '{directory}{name}' --submitted --sort new --time all -L {limit} --user '{name}' " \
                   f"--no-dupes --search-existing"

    print(f"Command being executed:\n`{command}`"
          "\n----------")
    subprocess.run(command, shell=True)

    print("Sleeping 10 seconds before automatically moving on")
    sleep(10)


def load_exclusions():
    exclusions = set()
    with open("exclusions.txt", "r") as file_in:
        text = file_in.read()
        exclusions = set(text.split("\n"))
    return exclusions


def main(args):
    main_dir = args.directory
    if main_dir[-1] != "/":
        main_dir += "/"
    if len(args.users):
        users = args.users.split(",")
        for user in users:
            start_dl(main_dir, user, args.limit)
    else: # default is to update everything in dirs
        # get exclusion dirs
        exclusions = load_exclusions()
        dirlist = sorted(scandir(main_dir), key=lambda x: x.name.lower())
        for directory in dirlist:
            if not directory.is_dir():
                continue
            if args.start != "" and args.start > directory.name.lower():
                continue
            if args.end != "" and args.end < directory.name.lower():
                print(f"Directory {directory.name} is after {args.end}, stopping.")
                break
            if directory.name in exclusions:
                continue
            start_dl(main_dir, directory.name, args.limit)


if __name__ == '__main__':
    args = parse()
    main(args)
