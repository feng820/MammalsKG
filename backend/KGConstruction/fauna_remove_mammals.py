import json
import sys
from merge_mammal import load_json, store_json


def get_key_taxon(all_mammals):
    taxon_key = {}
    for key in all_mammals:
        taxon = all_mammals[key]["taxonName"].lower().strip()
        taxon_key[taxon] = key

        if "subspecies" in all_mammals[key]:
            subspecies = all_mammals[key]["subspecies"]
            for subspecie in subspecies:
                subspecie_name = subspecie["taxonName"].lower().strip()
                subspecie_id = subspecie["id"]
                taxon_key[subspecie_name] = subspecie_id

    return taxon_key


def main(argv):
    all_mammals_json = "./all_mammals.json"
    ecoregion_class_json = "./Final_KG_data/ecoregion_class.json"

    all_mammals = load_json(all_mammals_json)
    taxon_key = get_key_taxon(all_mammals)
    ecoregion_class = load_json(ecoregion_class_json)

    for key in ecoregion_class:
        fauna = ecoregion_class[key]["fauna"]
        mammals = set(ecoregion_class[key]["mammals"]) # list

        new_fauna = [d for d in fauna if d.get('taxonName').lower().strip() not in taxon_key]
        mammal_all = set()
        for animal in fauna:
            if animal["taxonName"].lower().strip() in taxon_key:
                mammal_all.add(taxon_key[animal["taxonName"].lower().strip()])
        mammal_subs = mammal_all.difference(mammals)

        ecoregion_class[key]["fauna"] = new_fauna
        ecoregion_class[key]["mammals_subs"] = list(mammal_subs)

    store_json("./Final_KG_data/ecoregion_class_plus.json", ecoregion_class)


if __name__ == '__main__':
    main(sys.argv[1:])
