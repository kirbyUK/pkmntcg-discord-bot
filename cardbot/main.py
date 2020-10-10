"""Module defining the main entry point of the program, and argument parsing."""
import argparse
import sys

from cardbot.discord_client import client


# Process commandline arguments to get the Discord API token
def args() -> str:
    """
    Process commandline arguments to get the Discord API token.

    Available commandline arguments are one of:
    * -t / --token - Specify the token on the commandline
    * -f / --token-file - Specify the path to a file containing the token

    :returns: The Discord API token to use
    """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-t', '--token',
        help='The Discord API token'
    )
    group.add_argument(
        '-f', '--token-file',
        type=argparse.FileType('r'),
        help='A file containing the Discord API token'
    )
    args = parser.parse_args()

    if args.token:
        return args.token
    elif args.token_file:
        return args.token_file.readline().rstrip()
    else:
        print('Please specify a valid API token with -t or -f', file=sys.stderr)
        exit(1)


def main() -> None:
    """Program entry point."""
    token = args()
    client.run(token)


if __name__ == '__main__':
    main()
