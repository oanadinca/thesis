from blog1 import whatedsaid
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument("--url", type=str,
                        help="Please provide a blog url for data crawl!")
    args = parser.parse_args()
    if "whatedsaid" in args.url:
        whatedsaid.main(args)


if __name__ == "__main__":
    main()
