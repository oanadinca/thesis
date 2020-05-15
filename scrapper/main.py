from blog1 import whatedsaid
from blog2 import vickyloras
from blog3 import chiasuanchong
from argparse import ArgumentParser

from elastic_wrapper import ElasticWrapper


def main():
    parser = ArgumentParser()
    parser.add_argument("--url", type=str,
                        help="Please provide a blog url for data crawl!")
    es = ElasticWrapper()

    args = parser.parse_args()
    if "whatedsaid" in args.url:
        contributions = whatedsaid.main(args)
        for contribution in contributions:
            es.store_post(contribution)
    if "vickyloras" in args.url:
        vickyloras.main(args)
    if "chiasuanchong" in args.url:
        chiasuanchong.main(args)


if __name__ == "__main__":
    main()
