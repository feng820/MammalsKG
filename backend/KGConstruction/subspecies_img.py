import json
import sys
import requests
from eol_traits_crawling import pred_prey
from merge_mammal import load_json, store_json


def extract_subspecies_id(all_mammals):
    subspecie_names = []
    for key in all_mammals:
        species = all_mammals[key]
        if "subspecies" in species:
            subspecies = species["subspecies"]
            for subspecie in subspecies:
                subspecie_names.append(subspecie["name"])

    return subspecie_names


def main(argv):
    all_mammals_json = "./all_mammals.json"
    all_mammals = load_json(all_mammals_json)
    # print(all_mammals)
    subspecies_names = extract_subspecies_id(all_mammals)
    # TODO: 通过subspecie_names搜索图片


if __name__ == '__main__':
    main(sys.argv[1:])
