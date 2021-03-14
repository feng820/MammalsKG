import json
import sys
import requests
import lxml
from bs4 import BeautifulSoup


def parse(eol_id):
    raw_response = requests.get("https://eol.org/pages/" + eol_id + "/data")
    collection = {}
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
                if my_trait in trait.text.strip().lower():  # Format trait text in page to match with my trait
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
                            trait_mod = None
                            # collection[my_trait] = trait_val
                            collection.setdefault(my_trait, []).append(trait_val)

                        else:
                            trait_mod = trait_mod.text.strip()
                            # collection[my_trait] = (trait_val, trait_mod)
                            collection.setdefault(my_trait, []).append((trait_val, trait_mod))

                        tmp = tmp.find_next_sibling()
    else:
        print("Page not found")
    return collection


def main(argv):
    eol_id = "328338"
    single_page = parse(eol_id)
    # print(len(single_page))
    print(single_page)


if __name__ == "__main__":
    main(sys.argv[1:])
