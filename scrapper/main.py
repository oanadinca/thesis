from blog1 import whatedsaid
from blog2 import vickyloras
from blog3 import chiasuanchong
from argparse import ArgumentParser
from tweeter_posts import tweeter_crawler


def main():
    parser = ArgumentParser()
    parser.add_argument("--url", type=str,
                        help="Please provide a blog url for data crawl!")
    args = parser.parse_args()
    if "whatedsaid" in args.url:
        whatedsaid.main(args)
    if "vickyloras" in args.url:
        vickyloras.main(args)
    if "chiasuanchong" in args.url:
        chiasuanchong.main(args)

    # tweeter_crawler.main()


if __name__ == "__main__":
    main()
