import json


def get_combined_data():
    with open('kg_mammals.json', 'r') as f_in:
        combined_dict = json.load(f_in)
        return combined_dict


def separate_subspecies():
    combined_dict = get_combined_data()
    subspecies_dict = dict()
    for key, info_dict in combined_dict.items():
        subspecies_list = info_dict.get('subspecies', [])
        subspecies_ids = []
        for subspecies in subspecies_list:
            subspecies_ids.append(subspecies['id'])
            subspecies_dict[subspecies['id']] = {
                'name': subspecies['name'],
                'taxonName': subspecies['taxonName'],
                'location_info': subspecies['subspecies_location_info']
            }
        info_dict['subspecies'] = subspecies_ids

    with open('subspecies_class.json', 'w') as f_out1, open('kg_mammals.json', 'w') as f_out2:
        json.dump(subspecies_dict, f_out1)
        json.dump(combined_dict, f_out2)


def build_inverse_dict(combined_dict):
    inverse_dict = dict()
    for key, info_dict in combined_dict.items():
        inverse_dict[info_dict['taxonName']] = key
    return inverse_dict


def __separate_other_animals(key, info_dict, inverse_dict, non_mammal_dict):
    animal_list = info_dict.get(key, [])
    animal_ids = []
    for animal in animal_list:
        animal_id = str(animal['id'])
        animal_taxon_name = animal['canonicalName']
        if animal_taxon_name in inverse_dict:
            animal_ids.append(inverse_dict.get(animal_taxon_name))
        else:
            animal_id = "NM" + animal_id  # non mammals
            animal_ids.append(animal_id)
            non_mammal_dict[animal_id] = {
                'shortName': animal['shortName'],
                'taxonName': animal_taxon_name,
                'icon': animal['icon']
            }
        info_dict[key] = animal_ids


def separate_other_animals():
    combined_dict = get_combined_data()
    inverse_dict = build_inverse_dict(combined_dict)
    non_mammal_dict = dict()
    for key, info_dict in combined_dict.items():
        __separate_other_animals('predator', info_dict, inverse_dict, non_mammal_dict)
        __separate_other_animals('prey', info_dict, inverse_dict, non_mammal_dict)
        __separate_other_animals('competitor', info_dict, inverse_dict, non_mammal_dict)

    with open('non_species_class.json', 'w') as f_out1, open('kg_mammals.json', 'w') as f_out2:
        json.dump(non_mammal_dict, f_out1)
        json.dump(combined_dict, f_out2)


def separate_ecoregion():
    combined_dict = get_combined_data()
    for key, info_dict in combined_dict.items():
        ecoregions = info_dict.get('species_ecoregion_link', [])
        ecoregions_ids = []
        for ecoregion in ecoregions:
            ecoregions_ids.append(ecoregion[1])
        info_dict['ecoregion'] = ecoregions_ids
        info_dict.pop('eol_ecoregion', None)
        info_dict.pop('species_ecoregion_link', None)
    with open('kg_mammals.json', 'w') as f_out:
        json.dump(combined_dict, f_out)


if __name__ == '__main__':
    pass
