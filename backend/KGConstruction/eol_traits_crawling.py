import json
import sys
import requests
from bs4 import BeautifulSoup
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
    out_dict = {}
    for id in id_links:
        eol_id = os.path.basename(id_links[id])
        single_page = parse_traits(eol_id)
        if single_page:
            relations = pred_prey(eol_id)
            single_page.update(relations)
            out_dict[id] = single_page
            print(id + " crawled")
        else:
            print(id + " not crawled")
    outfile = open(eol_mammal_traits, "w")
    json.dump(out_dict, outfile)
    outfile.close()


def parse_traits(eol_id):
    raw_response = requests.get("https://eol.org/pages/" + eol_id + "/data")
    collection = {"eol_id": eol_id, "eol_mass": 0, "eol_length": 0, "eol_life_span": 0,
                  "eol_ecoregion": [], "eol_geographic_distribution": [], "eol_geographic_range":
                      None, "eol_habitat": []}

    if raw_response.status_code == 200:
        response = raw_response.content
        soup = BeautifulSoup(response, 'lxml')

        traits = soup.find_all("div", {"class": "data-section-head"})
        my_traits = ["mass", "length", "life span", "ecoregion", "geographic distribution "
                                                                 "includes", "geographic range "
                                                                             "(size of area)",
                     "habitat"]
        for trait in traits:
            for my_trait in my_traits:  # Find all traits to extract
                # Format trait text, make sure habitat breadth is not include!
                if my_trait in trait.h3.text.strip().lower() and trait.h3.text.strip().lower() != "habitat breadth"\
                        and trait.h3.text.strip().lower() != "body mass":
                    # in page to match with my trait
                    tmp = trait.find_next_sibling()
                    while tmp and tmp.name == "li":  # Make sure tmp.name is not None
                        trait_val = tmp.find('div', {'class': 'a js-data-val'})
                        # Check if trait val has link property or not
                        if trait_val:
                            trait_val = trait_val.text.strip()
                        else:
                            trait_val = tmp.find('div', {'class': 'trait-val'}).text.strip()

                        trait_mod = tmp.find('div', {'class': 'trait-mod'})
                        # dict val type is either str or tuple

                        if my_trait == "mass":
                            # 单位是kg
                            # trait_val = str(float(trait_val.replace(" g", "")) / 1000) + " kg"
                            if trait_val.endswith(" g"):
                                trait_val = round(float(trait_val.replace(" g", "")) / 1000, 3)
                            else:
                                trait_val = 0

                            if not collection["eol_mass"]:  # If "mass" is empty yet
                                if not trait_mod:
                                    collection["eol_mass"] = trait_val
                                else:
                                    # collection["eol_mass"] = trait_val + trait_mod
                                    collection["eol_mass"] = trait_val
                            else:
                                if trait_mod and trait_mod == "(adult)":
                                    print("Replace mass with (adult) as trait_mode")
                                    # collection["eol_mass"] = trait_val + trait_mod
                                    collection["eol_mass"] = trait_val
                        elif my_trait == "length":
                            # 单位是m
                            if trait_val.endswith(" mm"):
                                trait_val = round(float(trait_val.replace(" mm", "")) / 1000, 3)
                            elif trait_val.endswith(" m"):
                                trait_val = float(trait_val.replace(" m", ""))
                            else:
                                trait_val = 0

                            if not collection["eol_length"]:
                                if not trait_mod:
                                    collection["eol_length"] = trait_val
                                else:
                                    collection["eol_length"] = trait_val
                            else:
                                pass
                        elif my_trait == "life span":
                            # 单位是years, max life span
                            if trait_val.endswith(" months"):
                                trait_val = round(float(trait_val.replace(" months", "")) / 12, 1)
                            elif trait_val.endswith(" years"):
                                trait_val = float(trait_val.replace(" years", ""))
                            else:
                                trait_val = 0

                            if not collection["eol_life_span"]:
                                if not trait_mod:
                                    collection["eol_life_span"] = trait_val
                                else:
                                    collection["eol_life_span"] = trait_val
                            else:
                                pass
                        elif my_trait == "ecoregion":
                            collection["eol_ecoregion"].append(trait_val)
                        elif my_trait == "geographic distribution includes":
                            collection["eol_geographic_distribution"].append(trait_val)
                        elif my_trait == "geographic range (size of area)":
                            collection["eol_geographic_range"] = trait_val
                        elif my_trait == "habitat":
                            collection["eol_habitat"].append(trait_val)
                        else:
                            pass

                        tmp = tmp.find_next_sibling()

                elif trait.h3.text.strip().lower() == "habitat breadth":
                    pass
                else:
                    pass
    else:
        print("Page not found")
    return collection


def pred_prey(eol_id):
    single_pred_prey = {"img": None, "predator": [], "prey": [], "competitor": []}
    raw_response = requests.get("https://eol.org/api/pages/" + eol_id + "/pred_prey.json")

    try:
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
    except ValueError:
        print("Decoding JSON has failed")

    # If any fields don't exist, return key with empty list
    return single_pred_prey


def main(argv):
    eol_mammal_links_json = "./eol_mammal_link.json"
    eol_mammal_traits_json = "./eol_mammal_trait.json"

    id_links = load_json(eol_mammal_links_json)
    store_json(id_links, eol_mammal_traits_json)


if __name__ == "__main__":
    main(sys.argv[1:])
