import json
import sys
import requests
import lxml
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os.path


def load_json(eol_mammal_link_json):
    # Opening JSON file
    id_links = {}
    with open(eol_mammal_link_json) as json_file:
        data = json.load(json_file)
        for key in data:
            id_links[key] = data[key]

    json_file.close()

    return id_links


def store_json(id_links, eol_mammal_traits):
    with open(eol_mammal_traits, "w") as outfile:
        for id in id_links:
            eol_id = os.path.basename(id_links[id])  # String type id
            # eol_id = "328338"
            single_page = parse_traits(eol_id)
            if single_page:
                relations = pred_prey(eol_id)
                single_page.update(relations)
                outfile.write(json.dumps(single_page))
                outfile.write("\n")

        # json.dump(mammal_fields, outfile)
    outfile.close()


def parse_traits(eol_id):
    raw_response = requests.get("https://eol.org/pages/" + eol_id + "/data")
    collection = {"eol_id": eol_id, "mass": [], "length": [], "conservation status": [], "life span": [],
                  "ecoregion": [], "geographic distribution includes": [], "geographic range (size of area)": [],
                  "habitat": [], "latitude": [], "longitude": []}

    if raw_response.status_code == 200:
        response = raw_response.content
        soup = BeautifulSoup(response, 'lxml')

        traits = soup.find_all("div", {"class": "data-section-head"})
        my_traits = ["mass", "length", "conservation status", "life span", "ecoregion", "geographic distribution "
                                                                                        "includes", "geographic range "
                                                                                                    "(size of area)",
                     "habitat", "latitude", "longitude"]
        for trait in traits:
            for my_trait in my_traits:  # Find all traits to extract
                # Format trait text, make sure habitat breadth is not include!
                if my_trait in trait.h3.text.strip().lower() and trait.h3.text.strip().lower() != "habitat breadth":
                    # in page to match with my trait
                    tmp = trait.find_next_sibling()
                    while tmp.name == "li":
                        trait_val = tmp.find('div', {'class': 'a js-data-val'})
                        # Check if trait val has link property or not
                        if trait_val:
                            trait_val = trait_val.text.strip()
                        else:
                            trait_val = tmp.find('div', {'class': 'trait-val'}).text.strip()

                        trait_mod = tmp.find('div', {'class': 'trait-mod'})
                        # dict val type is either str or tuple
                        if not trait_mod:
                            collection[my_trait].append(trait_val)

                        else:
                            trait_mod = trait_mod.text.strip()
                            collection[my_trait].append((trait_val, trait_mod))

                        tmp = tmp.find_next_sibling()

                elif trait.h3.text.strip().lower() == "habitat breadth":
                    pass
                else:
                    pass
    else:
        print("Page not found")
    return collection


def pred_prey(eol_id):
    single_pred_prey = {"img": "", "predator": [], "prey": [], "competitor": []}
    raw_response = requests.get("https://eol.org/api/pages/" + eol_id + "/pred_prey.json")

    for data in raw_response.json()["nodes"]:
        group = data["group"]
        if group in ["predator", "prey", "competitor"]:  # dict keys
            single_pred_prey[group].append({"id": data["id"], "shortName": data["shortName"],
                                            "canonicalName": data["canonicalName"],
                                            "icon": data["icon"]})
        elif group == "source":  # current type is source (the target itself), store img instead
            single_pred_prey["img"] = data["icon"].replace("130x130.jpg", "580x360.jpg")  # convert img quality
        else:
            print("Unknown pred_prey type found" + group)
            pass
    # If any fields don't exist, return key with empty list
    return single_pred_prey


def main(argv):
    eol_mammal_links_json = "./eol_mammal_link.json"
    eol_mammal_traits_json = "./eol_mammal_trait.all"

    id_links = load_json(eol_mammal_links_json)
    store_json(id_links, eol_mammal_traits_json)

    # parse_traits("328338")


if __name__ == "__main__":
    main(sys.argv[1:])
