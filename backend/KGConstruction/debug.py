import json
import sys
import requests
from bs4 import BeautifulSoup
import os.path
from eol_traits_crawling import parse_traits


def main(argv):
    # print(parse_traits("46559376"))
    print(parse_traits("46559277"))


if __name__ == '__main__':
    main(sys.argv[1:])
