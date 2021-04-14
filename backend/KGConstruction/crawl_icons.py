import json
import wikipedia
from bs4 import BeautifulSoup
import requests


def crawl_icons(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        dictionary = json.load(f_in)
        for key, info_dict in dictionary.items():
            taxon_name = info_dict['taxonName']
            icon = info_dict.get('icon')
            if taxon_name and not icon:
                try:
                    page = wikipedia.page(taxon_name)
                    url = page.url
                except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError) as e:
                    print(e)
                if url:
                    resp = requests.get(url)
                    soup_obj = BeautifulSoup(resp.content, 'html.parser')
                    info_box = soup_obj.select('#mw-content-text > div.mw-parser-output > table.infobox > tbody > tr')
                    if len(info_box) > 0:
                        info_dict['url'] = url
                        print(taxon_name)
                        if len(info_box) >= 2:
                            image_location = info_box[1].select('td > a')
                            if len(image_location) > 0:
                                base_url = "https://en.wikipedia.org/"
                                image_location_url = base_url + image_location[0]['href']
                                image_location_resp = requests.get(image_location_url)
                                image_soup_obj = BeautifulSoup(image_location_resp.content, 'html.parser')
                                image_a = image_soup_obj.select('#file > a')
                                if len(image_a) > 0:
                                    info_dict['icon'] = "https:" + image_a[0]['href']

        json.dump(dictionary, f_out)


if __name__ == '__main__':
    crawl_icons("subspecies_class.json", "subspecies_class_v1.json")
