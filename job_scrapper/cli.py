import argparse
import pymongo
from typing import List


def crawl_site(website):
    pass

def crawl_sites(websites: List):

    for site in websites:
        crawl_site(site)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--site", help="Set the site or sites to run")

    args = parser.parse_args()

    if args.Output:
        print('testonly %' % args.Output)


if __name__ == "__main__":
    main()