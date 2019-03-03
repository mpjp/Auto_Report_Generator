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
            for title_number in mylist:

                test_case_table = get_table( title_number, soup )  
                
                result = {'TestCase':get_title(test_case_table, title_number), 'TestStep':'N/A', 
                        'TestData':'N/A', 'ExpectResult':'N/A', 'Description':'N/A'}
                        
                next_tb = test_case_table.find_next('table')

                while next_tb is not None and len(next_tb.find_all( 'h3', attrs={'class':'formtitle'} )) == 0:
                    if [td for td in next_tb.find_all('b') if td.text == 'Zephyr Teststep:']:
                        for index, label_name in enumerate(next_tb.find_all('td')):
                            if label_name.text == 'Zephyr Teststep:':
                                result.update(get_test_case_detail(next_tb, index))
                    if next_tb.find_all( 'td', attrs={'id': 'descriptionArea'}):
                        result.update(get_descriptioin(next_tb))
                    next_tb = next_tb.find_next('table')       

                total_data.append(result.copy())

        write_in_csv_file(total_data)
    except Exception as e:
        raise RuntimeError(getattr(e, 'message', repr(e)))

def get_table( title_number, soup ):
    all_titles = soup.find_all('h3', attrs={'class':'formtitle'})  # test_case_number
    return [title for title in all_titles if title_number in title.text][0]

def get_title( test_case_table, title_number ):
    return '['+ title_number + '] ' + test_case_table.find('a').text 

def get_descriptioin( description_table ):
    return {'Description': bef_text(description_table.text.strip())}

def get_test_case_detail( test_case_table, label_name_index ):    
    test_case_table = test_case_table.find_all("td")[label_name_index+1]
    get_tags = test_case_table.find_all("td")
    get_body = test_case_table.find_next("tbody")
    all_tags = get_body.find_all("tr")

    test_step = ''
    expection_result = ''
    test_step_number = ''
    test_data = ''

    if len(all_tags) == 1:
        test_step = get_tags[1].text
        test_data = get_tags[2].text
        expection_result = get_tags[3].text

    else:
        for t in all_tags:
            inner_text = t.find_all("td")
            for i, inn in enumerate( inner_text, start=1):
                if inn.text != '':    
                    if i == 1:
                        test_step_number = '['+ inn.text + ']'
                    elif i == 2:
                        test_step += test_step_number + inn.text + '\n'
                    elif i == 3:
                        test_data += test_step_number + inn.text + '\n'
                    elif i == 4:
                        expection_result += test_step_number + inn.text + '\n'    
    
    return {'TestStep': bef_text(test_step), 'TestData': bef_text(test_data),'ExpectResult': bef_text(expection_result) }

def bef_text( test ):
    return unicodedata.normalize("NFKD", test)
        
def write_in_csv_file(alist):
    with open('output.csv', 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['TestCase', 'TestStep', 'TestData', 'ExpectResult', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for x in range(len(alist)):
            writer.writerow(alist[x])

# read_data(['7142', '7141', '7140', '7094', '5262', '2555', '14745'])
# read_data(['5331'])  #lots steps
# read_data(['5343'])
# 5343
# read_data(['14745'])
# read_data(['7140'])  #no description
# read_data(['7196'])
# read_data(['7096'])
# read_data(['2555'])
# read_data(['15373', '14747', '7208'])