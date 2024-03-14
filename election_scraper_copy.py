"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Ivo Fiala
email: fiala.ivos@gmail.com
discord: ivofiala
"""

import sys
import csv
from requests import get
from bs4 import BeautifulSoup
from collections import defaultdict

def check_arguments(web_address:str):
    """
    checks the script argument - web address
    """
    home = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    answer = get(home)
    separatedHTML = BeautifulSoup(answer.text, features="html.parser")
    links = []
    for i in range(1, 15):
        selector = f'td[headers="t{i}sa3"] a'
        links.extend([link["href"] for link in separatedHTML.select(selector)])
    if web_address.split('/')[-1] not in links or web_address.rsplit('/', 1)[-2] != "https://volby.cz/pls/ps2017nss":
        print("incorrectly specified arguments, first argument - reference to the territorial unit (e.g. https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103), second argument - name of the output file")
        sys.exit()

def read_data(links:str, web_address:str, code:str, district:str):
    """
    reads data from small territorial units
    """
    total_numbers = {}
    separatedHTML = BeautifulSoup(links.text, features="html.parser")
    total_numbers["registered"] = (separatedHTML.select('td[headers="sa2"]'))[0].text if separatedHTML.select('td[headers="sa2"]') else None
    total_numbers["envelopes"] = (separatedHTML.select('td[headers="sa3"]'))[0].text if separatedHTML.select('td[headers="sa3"]') else None
    total_numbers["valid"] = (separatedHTML.select('td[headers="sa6"]'))[0].text if separatedHTML.select('td[headers="sa6"]')  else None
    if (total_numbers["registered"] == None and total_numbers["envelopes"] == None and total_numbers["valid"] == None):
        read_big_district(web_address, code, district)
    else:
        html_political_party = (separatedHTML.select('td[headers="t1sa1 t1sb2"]')) + (separatedHTML.select('td[headers="t2sa1 t2sb2"]'))
        html_number_votes = (separatedHTML.select('td[headers="t1sa2 t1sb3"]')) + (separatedHTML.select('td[headers="t2sa2 t2sb3"]'))
        political_party = prepare_text(html_political_party)
        number_votes = prepare_text(html_number_votes)
        results = dict(zip(political_party, number_votes))
        basic_info = {"code": code, "location:": district}
        final_list.append({**basic_info, **total_numbers, **results})

def read_data_big_district(links:str, code:str, district:str):
    """
    reads data from big territorial units
    """
    group_dict_votes = []
    group_total_numbers = []  
    for link in links:
        total_numbers={}
        web_address = "https://volby.cz/pls/ps2017nss/" + link
        answer = get(web_address)
        separatedHTML = BeautifulSoup(answer.text, features="html.parser")
        total_numbers["registered"] = (separatedHTML.select('td[headers="sa2"]'))[0].text if separatedHTML.select('td[headers="sa2"]') else None
        total_numbers["registered"] = ''.join(char for char in total_numbers["registered"] if char.isdigit())
        total_numbers["envelopes"] = (separatedHTML.select('td[headers="sa3"]'))[0].text if separatedHTML.select('td[headers="sa3"]') else None
        total_numbers["envelopes"] = ''.join(char for char in total_numbers["envelopes"] if char.isdigit())
        total_numbers["valid"] = (separatedHTML.select('td[headers="sa6"]'))[0].text if separatedHTML.select('td[headers="sa6"]')  else None
        total_numbers["valid"] = ''.join(char for char in total_numbers["valid"] if char.isdigit())
        group_total_numbers.append(total_numbers)
        #print (total_numbers)
        html_political_party = (separatedHTML.select('td[headers="t1sa1 t1sb2"]')) + (separatedHTML.select('td[headers="t2sa1 t2sb2"]'))
        html_number_votes = (separatedHTML.select('td[headers="t1sa2 t1sb3"]')) + (separatedHTML.select('td[headers="t2sa2 t2sb3"]'))
        political_party = prepare_text(html_political_party)
        number_votes = prepare_text(html_number_votes)
        group_dict_votes.append(dict(zip(political_party, [int(vote) for vote in number_votes])))
    # Initializing an empty dictionary for results
    result_dict_total_numbers = {}
    #print(result_dict_total_numbers)
    # Browsing dictionaries in the list
    for dictionary in group_total_numbers:
        for key, value in dictionary.items():
            try:
            # Converting a value to a number and adding it to the existing value of the resulting dictionary
                result_dict_total_numbers[key] = result_dict_total_numbers.get(key, 0) + int(value)
            except ValueError:
                print(f"Key value conversion error {key}")
    # Print the combined and summed dictionary
    #print(result_dict_total_numbers)
    result_dict_votes = defaultdict(int)
    for d in group_dict_votes:
        for key, value in d.items():
            result_dict_votes[key] += value
    result_dict_votes = dict(result_dict_votes)
    result_dict_total_numbers.update(result_dict_votes)
    #print({**{"code": code, "location:": district}, **result_dict_total_numbers})
    final_list.append({**{"code": code, "location:": district}, **result_dict_total_numbers})

def prepare_text(html:str):
    """
    gets data from html tags
    """
    text = []
    for string in html:
        if (string.text.strip() != "-"):
            text.append(string.text.strip())
    return text

def read_big_district(web_address:str, code:str, district:str):
    """
    prepares links for reading big territorial units
    """
    links = []
    href_values = []
    answer = get(web_address)
    separatedHTML = BeautifulSoup(answer.text, features="html.parser")
    links = separatedHTML.select(".cislo > a")
    href_values = [link.get('href') for link in links]
    read_data_big_district(href_values, code, district)

def write_csv(data:list, file_name:str):
    """
    writes the resulting data to a csv file
    """
    for dictionary in data:
        try:
            with open(file_name, 'a', newline='') as csv_soubor:
                fieldnames = list(dictionary.keys())
                writer = csv.DictWriter(csv_soubor, fieldnames=fieldnames)
                if csv_soubor.tell() == 0:
                    writer.writeheader()
                writer.writerow(dictionary)
        except Exception as e:
            print(f"Error when writing to CSV file: {e}")

if __name__ == "__main__":
    try:
        check_arguments(sys.argv[1])
    except IndexError:
        print(
        "To run the program, it is necessary to enter two arguments - a reference to the territorial unit and the name of the output file",
        "Write: python election_scraper.py 'link' 'filename' ", sep="\n")
        sys.exit()
    final_list = []
    web_address = sys.argv[1]
    file_name = sys.argv[2]
    answer = get(web_address)
    codes = []
    district = []
    links = []
    separatedHTML = BeautifulSoup(answer.text, features="html.parser")
    municipality_code = separatedHTML.select(".cislo > a")
    for code in municipality_code:
        codes.append(code.text)
    district_name = separatedHTML.select(".overflow_name")
    for name in district_name:
        district.append(name.text)
    address_district = separatedHTML.select(".center > a:nth-child(1) ")
    for link in address_district:
        links.append(link['href'])
    print ("STAHUJI DATA Z VYBRANÉHO URL: " + web_address)
    for link, code, district  in zip(links, codes, district) :
        web_address = "https://volby.cz/pls/ps2017nss/" + link
        answer = get(web_address)
        read_data(answer, web_address, code, district)
    print("UKLÁDÁM DO SOUBORU: ", file_name)
    write_csv(final_list, file_name)