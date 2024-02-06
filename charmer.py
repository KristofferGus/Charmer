import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd

from bs4 import BeautifulSoup
import re

def get_tabel_df(html_tabel_path):
    # Path to the HTML file containing the table
    html_file_path = html_tabel_path

    # Read the HTML file into a pandas DataFrame
    tables = pd.read_html(html_file_path)

    # Assuming the table you want is the first one in the file
    table_df = tables[0]

    # Now you have the table data in a DataFrame, you can manipulate it as needed


    # Sample HTML element
    html_element = '<td class="q-td text-left"><div class=""><div class="q-avatar" tags="[object Object],[object Object],[object Object],[object Object],[object Object],[object Object]" removeable="false" clickable="" style="font-size: 32px;"><div class="q-avatar__content row flex-center overflow-hidden"><img src="/api/v2/image/a.svg" cover=""><!----></div></div><div class="q-avatar" tags="[object Object],[object Object],[object Object],[object Object],[object Object],[object Object]" removeable="false" clickable="" style="font-size: 32px;"><div class="q-avatar__content row flex-center overflow-hidden"><img src="/api/v2/image/f.svg" cover=""></div></div><div class="q-avatar" tags="[object Object],[object Object],[object Object],[object Object],[object Object],[object Object]" removeable="false" clickable="" style="font-size: 32px;"><div class="q-avatar__content row flex-center overflow-hidden"><img src="/api/v2/image/m.svg" cover=""><!----></div></div><div class="q-avatar" tags="[object Object],[object Object],[object Object],[object Object],[object Object],[object Object]" removeable="false" clickable="" style="font-size: 32px;"><div class="q-avatar__content row flex-center overflow-hidden"><img src="/api/v2/image/td.svg" cover=""><!----></div></div><div class="q-avatar" tags="[object Object],[object Object],[object Object],[object Object],[object Object],[object Object]" removeable="false" clickable="" style="font-size: 32px;"><div class="q-avatar__content row flex-center overflow-hidden"><img src="/api/v2/image/tm.svg" cover=""></div></div><div class="q-avatar" tags="[object Object],[object Object],[object Object],[object Object],[object Object],[object Object]" removeable="false" clickable="" style="font-size: 32px;"><div class="q-avatar__content row flex-center overflow-hidden"><img src="/api/v2/image/v.svg" cover=""><!----></div></div></div></td>'

    # Parse the HTML element
    def get_image_names(html_element):
        soup = BeautifulSoup(html_element, 'html.parser')

        # Find all div elements with class 'q-avatar'
        avatar_divs = soup.find_all('div', class_='q-avatar')

        # Extract image names from the src attribute of each img tag
        image_names = []
        for avatar_div in avatar_divs:
            img_tags = avatar_div.find_all('img')
            for img_tag in img_tags:
                image_src = img_tag.get('src')
                image_name = image_src.split('/')[-1].split('.')[0]  # Extract image name from URL
                image_names.append(image_name)
        return image_names

    programs = []

    # Read the HTML file
    with open(html_file_path, 'r') as file:
        html_content = file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all tbody elements
    tbodies = soup.find_all('tbody')

    # Select the third td for every tr in each tbody
    for tbody in tbodies:
        rows = tbody.find_all('tr')
        for row in rows:
            # Check if the row has at least 3 td elements
            if len(row.find_all('td')) >= 3:
                third_td = row.find_all('td')[2]  # Selecting the third td element (index 2)
                programs.append(get_image_names(str(third_td)))  # Print the text content of the third td element
    programs
    table_df["Programs"] = programs
    table_df = table_df.drop(columns=['Logo', 'Favorites'], axis=1)
    table_df

    table_df["Looking for"] = [re.findall('[A-Z][^A-Z]*', s) for s in table_df["Looking for"]]
    offerings = []
    for s in table_df["Offering"]:
        if str(s) == "nan":
            offerings.append([])
            continue
        offerings.append(re.findall('[A-Z][^A-Z]*', s) )
    table_df["Offering"] = offerings
    return table_df

def find_company(table_df, programs, program_level, offering_types):
    good_companies = []
    for i in range(table_df.shape[0]):
        company = table_df.iloc[i]
        a = bool(set((company["Programs"])) & set(programs))
        a = a and bool(set(list(company["Looking for"])) & set(program_level))
        a = a and bool(set(list(company["Offering"])) & set(offering_types))
        if a:
            good_companies.append(company["Name"])
    return good_companies

