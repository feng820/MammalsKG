import json


def load_wiki():
    mammal_dict = dict()
    with open('wiki_species.json', 'r') as f_in:
        json_list = json.load(f_in)
        for entry in json_list:
            mammal_id = entry['species'].split('entity/')[1]
            species_dict = mammal_dict.get(mammal_id, dict())
            species_dict['name'] = entry['speciesLabel']
            species_dict['status'] = entry['statusLabel']
            species_dict['taxonName'] = entry['taxonName']
            common_names = species_dict.get('commonNames', [])
            if len(common_names) == 0:
                species_dict.update({'commonNames': common_names})

            if entry['commonName'] not in common_names:
                common_names.append(entry['commonName'])

            mammal_dict.update({mammal_id: species_dict})

    with open('wiki_subspecies.json') as f_in, open('all_mammals.json', 'w') as f_out:
        json_list = json.load(f_in)
        for entry in json_list:
            mammal_id = entry['species'].split('entity/')[1]
            species_dict = mammal_dict.get(mammal_id, None)
            if species_dict:
                subspecies = species_dict.get('subspecies', [])
                if len(subspecies) == 0:
                    species_dict.update({'subspecies': subspecies})
                subspecies.append({
                    "id": entry['subspecies'].split('entity/')[1],
                    "name": entry['subspeciesLabel'],
                    "taxonName": entry['taxonName'],
                    "status": entry.get('statusLabel')
                })
        json.dump(mammal_dict, f_out)


if __name__ == '__main__':
    load_wiki()
