import json
import sys
import re


def load_json(input_json):
    with open(input_json) as json_file:
        id_data = json.load(json_file)
    json_file.close()
    return id_data


def store_json(out_json, all_mammals):
    out = open(out_json, 'w')
    json.dump(all_mammals, out)
    out.close()


def get_key_taxon(all_mammals):
    taxon_key = {}
    for key in all_mammals:
        # Lower all taxonName
        taxon = all_mammals[key]["taxonName"].lower().strip()
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
    for key in adw_species_info:  # TODO: check whitespace
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
            s = adw_species_info[key]["Range_mass"].replace(",", "").strip()
            last = s.split()[-1]
            if last == "g":
                l = extract_nums(s, 1000)
            # "Range_mass": "115 (high)  kg"
            # "Range_mass": "males: 3,800 females: 1,800 (high)  kg"
            elif last == "kg":
                l = extract_nums(s, 1)
            else:
                l = []

            if len(l) == 0:
                pass
            elif len(l) == 1:
                l = [l[0], l[0]]
            elif len(l) == 2:
                l.sort()
            else:
                print(key + " Range_mass cannot has 3+ numbers")
                l = []
            adw_species_info[key]["Range_mass"] = l
        else:
            adw_species_info[key]["Range_mass"] = []
        if "Range_length" in adw_species_info[key]:
            s = adw_species_info[key]["Range_length"].replace(",", "").strip()
            last = s.split()[-1]
            if last == "mm":
                l = extract_nums(s, 1000)
            elif last == "cm":
                l = extract_nums(s, 100)
            elif last == "m":
                l = extract_nums(s, 1)
            else:
                l = []

            if len(l) == 0:
                pass
            elif len(l) == 1:
                l = [l[0], [0]]
            elif len(l) == 2:
                l.sort()
            else:
                print(key + " Range_length cannot has 3+ numbers")
                l = []
            adw_species_info[key]["Range_length"] = l
        else:
            adw_species_info[key]["Range_length"] = []
        if "Average_lifespan_wild" in adw_species_info[key]:
            s = adw_species_info[key]["Average_lifespan_wild"].replace(",", "").strip()
            last = s.strip()[-1]
            if last == "years":
                l = extract_nums(s, 1)
            elif last == "months":  # TODO: check correct
                l = extract_nums(s, 12)
            else:
                l = []

            if len(l) == 0:
                l = 0
            elif len(l) == 1:
                l = l[0]
            else:
                print(key + " Average_lifespan_wild cannot has 2+ numbers")
                l = 0
            adw_species_info[key]["Average_lifespan_wild"] = l
        else:
            adw_species_info[key]["Average_lifespan_wild"] = 0
        if "Average_lifespan_captivity" in adw_species_info[key]:
            s = adw_species_info[key]["Average_lifespan_captivity"].replace(",", "").strip()
            last = s.strip()[-1]
            if last == "years":
                l = extract_nums(s, 1)
            elif last == "months":
                l = extract_nums(s, 12)
            else:
                l = []

            if len(l) == 0:
                l = 0
            elif len(l) == 1:
                l = l[0]
            else:
                print(key + " Average_lifespan_captivity cannot has 2+ numbers")
                l = 0
            adw_species_info[key]["Average_lifespan_captivity"] = l
        else:
            adw_species_info[key]["Average_lifespan_captivity"] = 0
        # Delete Known_Predators
        adw_species_info[key].pop("Known_Predators", None)

    return adw_species_info


def extract_nums(s, precision):
    l = []
    for t in s.split():
        try:
            l.append(round(float(t) / precision, 3))
        except ValueError:
            pass
    return l


def update(all_mammals, eol_mammal_trait, adw_species_info, subspecies_location_info, species_ecoregion_link):
    for key in all_mammals:
        if key in eol_mammal_trait:
            all_mammals[key].update(eol_mammal_trait[key])
        else:
            print(key + " not exist in eol")
            # del all_mammals[key]  # If key not found in eol_mammal_trait_json, remove it
            all_mammals[key].update({"eol_id": key, "eol_mass": 0, "eol_length": 0, "eol_life_span": 0,
                                     "eol_ecoregion": [], "eol_geographic_distribution": [], "eol_geographic_range":
                                         None, "eol_habitat": [], "img": None, "predator": [], "prey": [],
                                     "competitor": []})
        if key in adw_species_info:
            all_mammals[key].update(adw_species_info[key])
        else:
            # print(key + " not exist in adw")
            all_mammals[key].update({"Habitat_Regions": [], "Terrestrial_Biomes": [], "Communication_Channel": [],
                                     "Primary_Diet": [], "Plant_Foods": [], "Animal_Foods": [], "Key_Behaviors": [],
                                     "Wetlands": [], "Range_mass": [], "Range_length": [], "Average_lifespan_wild":
                                         0, "Average_lifespan_captivity": 0})
        for subspecie in all_mammals[key]["subspecies"]:
            if subspecie["id"] in subspecies_location_info:
                subspecie.update({"subspecies_location_info": subspecies_location_info[subspecie["id"]]})
            else:
                print("subspecie key" + subspecie["id"] + "not exist in subspecies_location_info")
                subspecie.update({"subspecies_location_info": []})
        if key in species_ecoregion_link:
            all_mammals[key].update({"species_ecoregion_link": species_ecoregion_link[key]})
        else:
            print(key + " not exist in species_ecoregion_link")
            all_mammals[key].update({"species_ecoregion_link": []})

    return all_mammals


def check_ecoregion_info_plus(ecoregion_info_plus, taxon_key):
    for key in ecoregion_info_plus:
        faunas = ecoregion_info_plus[key]["fauna"]

        mammal_ids = {"mammals": []}
        for fauna in faunas:
            taxon_name = fauna["taxonName"].lower().strip()
            if taxon_name in taxon_key:
                mammal_ids["mammals"].append(taxon_key[taxon_name])
                # TODO: remove all mammals from faunas?

        ecoregion_info_plus[key].update(mammal_ids)

    return ecoregion_info_plus


def main(argv):
    all_mammals_json = "./all_mammals.json"
    eol_mammal_trait_json = "./eol_mammal_trait.json"
    adw_species_info_json = "./adw_species_info.json"
    subspecies_location_info_json = "./subspecies_location_info.json"
    species_ecoregion_link_json = "./species_ecoregion_link.json"
    ecoregion_info_plus_json = "./ecoregion_info_plus.json"
    out_json = "./kg_mammals.json"

    all_mammals = load_json(all_mammals_json)
    taxon_key = get_key_taxon(all_mammals)
    all_mammals = check_all_mammals(all_mammals)
    eol_mammal_trait = load_json(eol_mammal_trait_json)
    adw_species_info = load_json(adw_species_info_json)
    adw_species_info = check_adw_species_info(adw_species_info)
    subspecies_location_info = load_json(subspecies_location_info_json)
    species_ecoregion_link = load_json(species_ecoregion_link_json)
    kg_mammals = update(all_mammals, eol_mammal_trait, adw_species_info, subspecies_location_info,
                       species_ecoregion_link)
    store_json(out_json, kg_mammals)

    ecoregion_info_plus = load_json(ecoregion_info_plus_json)
    ecoregion_info_plus = check_ecoregion_info_plus(ecoregion_info_plus, taxon_key)
    store_json(ecoregion_info_plus_json, ecoregion_info_plus)


if __name__ == "__main__":
    main(sys.argv[1:])
