from bs4 import BeautifulSoup
import requests
import json


def extract_keywords(key_tag, soup_obj, adw_dict):
    extracted_keywords_name = [
        "Habitat Regions",
        "Terrestrial Biomes",
        "Wetlands",
        "Communication Channels",
        "Primary Diet",
        "Key Behaviors",
        "Plant Foods",
        "Animal Foods"
    ]

    section = soup_obj.select(key_tag)
    if len(section) > 0:
        section_parent = section[0].parent
        keywords_list = section_parent.select('ul.keywords.donthyphenate')
        for keyword_section in keywords_list:
            li_lists = keyword_section.select('li')
            header_key = None
            content = []
            for i in range(len(li_lists)):
                if i == 0:
                    header = li_lists[i].text
                    if header not in extracted_keywords_name:
                        break
                    header_key = header.replace(' ', '_')
                else:
                    tag = li_lists[i].find('a')
                    if not tag:
                        tag = li_lists[i].find('span')
                    content.append(tag.text)
            if header_key:
                adw_dict[header_key] = content


def crawl():
    base_url = "https://animaldiversity.org"
    extracted_attribute_name = [
        'Range mass',
        'Range length',
        'Average lifespan',
        'Known Predators'
    ]
    with open("all_mammals.json", 'r') as f_in:
        all_species_dict = json.load(f_in)

    adw_all_species_dict = dict()
    cnt = 0
    for species_id, species_dict in all_species_dict.items():
        taxon_name = species_dict['taxonName']
        link = base_url + '/search/?q=' + taxon_name + '&feature=INFORMATION'
        resp = requests.get(link)
        soup_obj = BeautifulSoup(resp.content, 'html.parser')
        search_results = soup_obj.select('#wrap > div > div > div.span7_5.blahblahblah.main > div.inner-wrap '
                                         '> section > div.results > ul > li')
        species_adw_dict = dict()
        if len(search_results) > 0:
            target_url = base_url + search_results[0].select('div.result > a')[0]['href']
            detail_info_resp = requests.get(target_url)
            if 'classification' in target_url:
                continue
            print(target_url)
            if detail_info_resp.status_code == 200:
                detail_soup_obj = BeautifulSoup(detail_info_resp.content, 'html.parser')

                # Habitat
                extract_keywords('#habitat', detail_soup_obj, species_adw_dict)

                # Communication
                extract_keywords('#communication', detail_soup_obj, species_adw_dict)

                # Food Habits
                extract_keywords('#food_habits', detail_soup_obj, species_adw_dict)

                # behavior
                extract_keywords('#behavior', detail_soup_obj, species_adw_dict)

                # Physical Description
                physical_description_section = detail_soup_obj.select('#physical_description')
                if len(physical_description_section) > 0:
                    section_parent = physical_description_section[0].parent
                    attr_list = section_parent.select('ul.aside > li')
                    for attr in attr_list:
                        attr_header = attr.find('dt').text
                        if attr_header in extracted_attribute_name:
                            attr_content = attr.select('dd')[0].text
                            species_adw_dict[attr_header.replace(' ', '_')] = attr_content

                # Lifespan/Longevity
                lifespan_section = detail_soup_obj.select('#lifespan_longevity')
                if len(lifespan_section) > 0:
                    section_parent = lifespan_section[0].parent
                    attr_list = section_parent.select('ul.aside > li')
                    for attr in attr_list:
                        attr_header = attr.find('dt').text.split('Status:')
                        if attr_header[0] in extracted_attribute_name:
                            status = attr_header[1].strip()
                            attr_content = attr.select('dd')[0].text
                            species_adw_dict[attr_header[0].replace(' ', '_') + '_' + status] = attr_content

                # Predation
                predation_section = detail_soup_obj.select('#predation')
                if len(predation_section) > 0:
                    section_parent = predation_section[0].parent
                    attr_list = section_parent.select('ul.aside > li')
                    for attr in attr_list:
                        attr_header = attr.find('dt').text
                        if attr_header in extracted_attribute_name:
                            predators = attr.select('dd > ul > li')
                            content_list = []
                            for predator in predators:
                                s = predator.text
                                common_name = s[:s.find("(")]
                                taxon_name = s[s.find("(") + 1:s.find(")")]
                                content_list.append({
                                    'name': common_name,
                                    'taxonName': taxon_name
                                })
                            species_adw_dict[attr_header.replace(' ', '_')] = content_list

        adw_all_species_dict[species_id] = species_adw_dict

        cnt += 1
        print(cnt)

    with open("adw_species_info.json", 'w') as f_out:
        print(len(adw_all_species_dict))
        json.dump(adw_all_species_dict, f_out)


if __name__ == '__main__':
    crawl()
