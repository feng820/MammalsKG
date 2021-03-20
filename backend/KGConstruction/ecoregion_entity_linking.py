import json
from strsimpy import Levenshtein


def link_ecoregion():
    species_ecoregion_link_dict = dict()
    levenshtein_obj = Levenshtein()
    with open('ecoregion_info.json', 'r') as f_in, open('eol_mammal_trait.json', 'r') as f_in2, \
            open('all_mammals.json') as f_in3:
        ecoregion_info_dict = json.load(f_in)
        eol_mammal_dict = json.load(f_in2)
        all_mammals_info_dict = json.load(f_in3)

        cnt = 0
        for key, info_dict in all_mammals_info_dict.items():
            print(cnt)
            cnt += 1
            species_eol_info = eol_mammal_dict.get(key)
            temp_arr = []
            if species_eol_info:
                species_ecoregions = species_eol_info.get('eol_ecoregion', [])
                for ecoregion_name in species_ecoregions:
                    ecoregion_key = search_ecoregion(ecoregion_name, ecoregion_info_dict, levenshtein_obj)
                    if ecoregion_key:
                        temp_arr.append([ecoregion_name, ecoregion_key])
            species_ecoregion_link_dict[key] = temp_arr

    with open('species_ecoregion_link.json', 'w') as f_out:
        json.dump(species_ecoregion_link_dict, f_out)


def search_ecoregion(search_name, ecoregion_info_dict, levenshtein_obj):
    dist = -1
    target_key = None
    for key, info_dict in ecoregion_info_dict.items():
        name = info_dict['name']

        levenshtein_dist = ecoregion_distance(name, search_name, levenshtein_obj)
        if dist < 0:
            dist = levenshtein_dist
            target_key = key
        else:
            if levenshtein_dist < dist:
                dist = levenshtein_dist
                target_key = key

    return target_key


def ecoregion_distance(n1, n2, levenshtein_obj):
    return levenshtein_obj.distance(n1.lower(), n2.lower())


if __name__ == '__main__':
    link_ecoregion()
