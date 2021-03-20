import json
import sys
import re


def load_json(input_json):
    with open(input_json) as json_file:
        id_data = json.load(json_file)
    json_file.close()
    return id_data


def get_key_taxon(all_mammals):
    taxon_key = {}
    for key in all_mammals:
        taxon = all_mammals[key]["taxonName"]
        taxon_key[taxon] = key
    return taxon_key


def check_all_mammals(all_mammals):
    for key in all_mammals:
        if "name" not in all_mammals[key]:
            all_mammals[key]["name"] = None
        if "status" not in all_mammals[key]:
            all_mammals[key]["status"] = None
        if "taxonName" not in all_mammals[key]:
            all_mammals[key]["taxonName"] = None
        if "commonNames" not in all_mammals[key]:
            all_mammals[key]["commonNames"] = []
        if "subspecies" not in all_mammals[key]:
            all_mammals[key]["subspecies"] = []
    return all_mammals


def check_adw_species_info(adw_species_info):
    for key in adw_species_info:
        if "Habitat_Regions" not in adw_species_info[key]:
            adw_species_info[key]["Habitat_Regions"] = []
        if "Terrestrial_Biomes" not in adw_species_info[key]:
            adw_species_info[key]["Terrestrial_Biomes"] = []
        if "Communication_Channel" not in adw_species_info[key]:
            adw_species_info[key]["Communication_Channel"] = []
        if "Primary_Diet" not in adw_species_info[key]:
            adw_species_info[key]["Primary_Diet"] = []
        if "Plant_Foods" not in adw_species_info[key]:
            adw_species_info[key]["Plant_Foods"] = []
        if "Animal_Foods" not in adw_species_info[key]:
            adw_species_info[key]["Animal_Foods"] = []
        if "Key_Behaviors" not in adw_species_info[key]:
            adw_species_info[key]["Key_Behaviors"] = []
        if "Wetlands" not in adw_species_info[key]:
            adw_species_info[key]["Wetlands"] = []
        if "Range_mass" in adw_species_info[key]:
            s = adw_species_info[key]["Range_mass"]
            l = []
            if s[-2:] == "g":
                for t in s.split():
                    try:
                        l.append(round(float(t) / 1000, 3))
                    except ValueError:
                        pass
                adw_species_info[key]["Range_mass"] = l
            # "Range_mass": "115 (high)  kg"
            # "Range_mass": "males: 3,800 females: 1,800 (high)  kg"
            elif s[-2:] == "kg":

        else:
            adw_species_info[key]["Range_mass"] = []
        if "Range_length" in adw_species_info[key]:
            s = adw_species_info[key]["Range_length"]
            l = []
            for t in s.split():
                try:
                    l.append(round(float(t) / 100, 3))
                except ValueError:
                    pass
            adw_species_info[key]["Range_length"] = l
        else:
            adw_species_info[key]["Range_length"] = []
        if "Average_lifespan_wild" in adw_species_info[key]:





def update(all_mammals, to_merge):
    for key in all_mammals:
        if key in to_merge:
            all_mammals[key].update(to_merge[key])
        else:
            # print(key)
            del all_mammals[key]  # If key not found in eol_mammal_trait_json, remove it
            # all_mammals[key].update({"eol_id": None, "eol_mass": 0, "eol_length": 0, "eol_life_span": 0,
            #                          "eol_ecoregion": [], "eol_geographic_distribution": [], "eol_geographic_range":
            #                              None, "eol_habitat": [], "img": None, "predator": [], "prey": [],
            #                          "competitor": []})
    return all_mammals


def main(argv):
    all_mammals_json = "./all_mammals.json"
    eol_mammal_trait_json = "./eol_mammal_trait.json"
    adw_species_info_json = "./adw_species_info.json"
    subspecies_location_info_json = "./subspecies_location_info.json"
    species_ecoregion_link_json = "./species_ecoregion_link.json"

    all_mammals = load_json(all_mammals_json)
    taxon_key = get_key_taxon(all_mammals)
    # print(taxon_key)
    all_mammals = check_all_mammals(all_mammals)
    # print(all_mammals)
    eol_mammal_trait = load_json(eol_mammal_trait_json)
    # print(eol_mammal_trait)

    adw_species_info = load_json(adw_species_info_json)
    adw_species_info = check_adw_species_info(adw_species_info)
    all_mammals = update(all_mammals, eol_mammal_trait)
    # print(all_mammals)


if __name__ == "__main__":
    main(sys.argv[1:])
