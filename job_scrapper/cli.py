import argparse
import pymongo
from typing import List


def crawl_site(website) -> bool:
    success = create_task(website)
    return success

def crawl_sites(websites: List):

    for site in websites:
        crawl_site(site)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--site", help="Set the site or sites to run")

    args = parser.parse_args()

    if args.site:
        print('testonly %' % args.site)


if __name__ == "__main__":
    main()