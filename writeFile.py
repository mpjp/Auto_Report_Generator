from bs4 import BeautifulSoup
import re
import csv
import unicodedata

def read_data(mylist=[], *test_cases):
    total_data = []

    try:
        with open("Items.html", "r", encoding="utf-8") as f:
            contents = f.read()
            soup = BeautifulSoup(contents, 'lxml')

            for test_case_number in mylist:
                elePath = soup.find(text=re.compile(test_case_number))  # test_case_number
                title_path = elePath.find_next_siblings("a")
                title = '[TMD-%s]' % test_case_number + " " + title_path[0].string
                print(title)
                curr = elePath.find_next("table").find_next("table")

                if curr.find_all("b")[0].text == 'Zephyr Teststep:':
                    curr_table = curr.find_all('table')[0]
                else:
                    curr_table = curr.find_all("table")[1]

                get_tags = curr_table.find_all("td")

                test_step = unicodedata.normalize("NFKD", get_tags[1].text)
                test_data = unicodedata.normalize("NFKD",get_tags[2].text)
                expection_result = unicodedata.normalize("NFKD",get_tags[3].text)
                description = unicodedata.normalize("NFKD",curr.find_next_siblings("table")[1].find('td', {'id': 'descriptionArea'}).text)
                all_data = {}
                all_data.update({'TestCase': title, 'TestStep': test_step, 'TestData': test_data,
                                'ExpectResult': expection_result, 'Description': description})
                total_data.append(all_data)
        write_in_csv_file(total_data)
    except Exception as e:
        raise RuntimeError(getattr(e, 'message', repr(e)))
        
def write_in_csv_file(alist):
    with open('output.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['TestCase', 'TestStep', 'TestData', 'ExpectResult', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for x in range(len(alist)):
            writer.writerow(alist[x])


