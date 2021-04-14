import json
import sys
import requests
from bs4 import BeautifulSoup
import os.path
from eol_traits_crawling import parse_traits


def main(argv):
    # print(parse_traits("328605"))
    # print(parse_traits("289808"))
    # print(parse_traits("311503"))
    # print(parse_traits("327285"))
    print(parse_traits("328825"))
    # print(parse_traits("126944"))


if __name__ == '__main__':
    main(sys.argv[1:])
