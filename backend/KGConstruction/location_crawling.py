from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import chromedriver_binary


def get_mammals_key():
    base_url = "https://www.gbif.org/species/search?q="

    with open("subspecies_location_key.json", 'r') as f_in:
        subspecies_location_key_dict = json.load(f_in)
        print(len(subspecies_location_key_dict))

    with open('all_mammals.json', 'r') as f_in:
        mammals_dict = json.load(f_in)
        for mammal_id, species_dict in mammals_dict.items():
            subspecies_list = species_dict.get('subspecies', [])
            for subspecies_dict in subspecies_list:
                subspecies_id = subspecies_dict.get('id')
                taxon_name = subspecies_dict.get('taxonName')
                if subspecies_id and taxon_name and subspecies_id not in subspecies_location_key_dict:
                    location_url = base_url + taxon_name
                    driver = webdriver.Chrome()
                    driver.maximize_window()  # For maximizing window
                    driver.implicitly_wait(5)  # gives an implicit wait for 5 seconds
                    driver.get(location_url)
                    try:
                        found = WebDriverWait(driver, 10).until(
                            EC.visibility_of(
                                driver.find_element(By.CLASS_NAME, "searchCard__headline")
                            )
                        )
                        detail_url = found.find_element(By.TAG_NAME, 'a').get_attribute('href')
                        mammal_key = detail_url.split('species/')[1]
                        subspecies_location_key_dict.update({subspecies_id: mammal_key})
                    except (NoSuchElementException, WebDriverException) as e:
                        print(e.msg)
                        subspecies_location_key_dict.update({subspecies_id: "-1"})
                    finally:
                        driver.close()

    with open("subspecies_location_key.json", 'w') as f_out:
        json.dump(subspecies_location_key_dict, f_out)


def crawl_locations():
    with open("subspecies_location_key.json", 'r') as f_in1, open("subspecies_location_info.json", 'r') as f_in2:
        subspecies_location_key_dict = json.load(f_in1)
        subspecies_location_info_dict = json.load(f_in2)
        print(len(subspecies_location_info_dict))

    cnt = 0
    for subspecies_id, location_key in subspecies_location_key_dict.items():
        if subspecies_id in subspecies_location_info_dict:
            continue
        url = "https://www.gbif.org/occurrence/search?taxon_key=" + location_key
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="termsOfUse"]/div/div[2]/a[2]'))).click()

            found = WebDriverWait(driver, 10).until(
                EC.visibility_of(
                    driver.find_element(By.TAG_NAME, "tbody")
                )
            )

            coordinates_set = set()
            location_info = subspecies_location_info_dict.get(subspecies_id, [])
            for row in found.find_elements(By.TAG_NAME, "tr"):
                try:
                    occurrence_country = row.find_element_by_css_selector("td:nth-child(3) > a").text
                    coordinate = row.find_element_by_css_selector("td:nth-child(4) > a").text
                    occurrence_date = row.find_element_by_css_selector("td:nth-child(5) > a").text

                    if coordinate and coordinate not in coordinates_set:
                        location_info.append([occurrence_country, occurrence_date, coordinate])
                        coordinates_set.add(coordinate)

                except (NoSuchElementException, WebDriverException) as e:
                    print(e.msg)
            print(cnt)
            cnt += 1
            subspecies_location_info_dict.update({subspecies_id: location_info})
        except (NoSuchElementException, WebDriverException) as e:
            print(e.msg)
            subspecies_location_info_dict.update({subspecies_id: []})
        finally:
            driver.close()

    with open("subspecies_location_info.json", 'w') as f_out:
        print(len(subspecies_location_key_dict))
        print(len(subspecies_location_info_dict))
        json.dump(subspecies_location_info_dict, f_out)


if __name__ == '__main__':
    crawl_locations()
