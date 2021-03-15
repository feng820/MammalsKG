import wikipedia
from bs4 import BeautifulSoup
import requests
import json


def preprocess():
    with open('wiki_ecoregion.json', 'r') as f_in, open('ecoregion_list.json', 'w') as f_out:
        ecoregion_dict = json.load(f_in)
        output_dict = dict()
        for entry in ecoregion_dict:
            wiki_id = entry['region'].split('entity/')[1]
            label = entry['regionLabel']
            if wiki_id != label and wiki_id not in output_dict:
                coordinates = entry.get('coordinates')
                if coordinates:
                    coord_list = coordinates[coordinates.find('(') + 1:coordinates.find(')')].split(' ')
                    s1 = coord_list[1]
                    s2 = coord_list[0]
                    if '-' in s1:
                        s1 = s1.replace('-', '')
                        s1 += 'S'
                    else:
                        s1 += 'N'
                    if '-' in s2:
                        s2 = s2.replace('-', '')
                        s2 += 'W'
                    else:
                        s2 += 'E'
                    coordinates = [s1, s2]
                output_dict[wiki_id] = {
                    'name': label,
                    'coordinates': coordinates
                }
        json.dump(output_dict, f_out)


def crawl_wikipedia():
    attributes_list = ['Biome', 'Area', 'Country', 'Conservation status']
    with open('ecoregion_list.json', 'r') as f_in, open('ecoregion_info.json', 'w') as f_out:
        ecoregion_dict = json.load(f_in)
        ecoregion_info_dict = dict()
        print(len(ecoregion_dict))
        for ecoregion_id, value_dict in ecoregion_dict.items():
            ecoregion_name = value_dict['name']
            ecoregion_coordinates = value_dict.get('coordinates')
            url = None
            try:
                page = wikipedia.page(ecoregion_name)
                url = page.url
            except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError)  as e:
                print(e)
            if url:
                print(ecoregion_name, url)
                resp = requests.get(url)
                soup_obj = BeautifulSoup(resp.content, 'html.parser')

                info_box = soup_obj.select('#mw-content-text > div.mw-parser-output > table.infobox > tbody > tr')
                if len(info_box) > 0:
                    summary = page.summary if page.summary else None
                    if summary:
                        value_dict['summary'] = summary
                    image = page.images[0] if len(page.images) > 0 else None
                    if image:
                        value_dict['image'] = image
                    for info in info_box:
                        attribute = info.find('th')
                        content = info.find('td')
                        if attribute and content and attribute.text in attributes_list:
                            value_dict[attribute.text.replace(' ', '_')] = content.text

                    coordinates_span = soup_obj.select('#coordinates > span > a > span.geo-default > span.geo-dec')
                    if len(coordinates_span) > 0:
                        coordinates = coordinates_span[0].text
                        if not ecoregion_coordinates:
                            value_dict['coordinates'] = coordinates

                    ecoregion_info_dict[ecoregion_id] = value_dict

        print(len(ecoregion_info_dict))
        json.dump(ecoregion_info_dict, f_out)


if __name__ == '__main__':
    crawl_wikipedia()
