import json
import sys
import requests


def load_json(all_mammals_json):
    # Opening JSON file
    id_taxons = {}
    with open(all_mammals_json) as json_file:
        data = json.load(json_file)
        for key in data:
            id_taxons[key] = data[key]["taxonName"]

    json_file.close()

    return id_taxons


def store_json(mammal_fields, eol_mammal_links_json):
    with open(eol_mammal_links_json, "w") as outfile:
        json.dump(mammal_fields, outfile)
    outfile.close()


def request_eol(id_taxons):
    results = {}
    for key in id_taxons:
        taxon = id_taxons[key]
        request_taxon = id_taxons[key].lower().replace(" ", "%2B")
        raw_response = requests.get("https://eol.org/api/search/1.0.json?q=" + request_taxon + "&page=1&exact=true&key=")
        url = None
        for data in raw_response.json()["results"]:
            if data["title"].lower() == taxon.lower():
                url = data["link"]
                results[key] = url
                print("\n" + taxon + " found")
                break
        if not url:
            print('\n' + taxon + " not found...")

    return results


def main(argv):
    all_mammals_json = "./all_mammals.json"
    eol_mammal_links_json = "./eol_mammal_link.json"

    id_taxons = load_json(all_mammals_json)
    mammal_urls = request_eol(id_taxons)

    store_json(mammal_urls, eol_mammal_links_json)


if __name__ == "__main__":
    main(sys.argv[1:])
