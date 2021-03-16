import wikipedia
from bs4 import BeautifulSoup
import requests
import json
import sys


def parse_page(name):
    page = wikipedia.page("Southeastern conifer forests")
    # print(ny.url)



def main(argv):
    ecoregion_info = "./ecoregion_info.json"

    name = "New York"
    parse_page(name)


if __name__ == "__main__":
    main(sys.argv[1:])
