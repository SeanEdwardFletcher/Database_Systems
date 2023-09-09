# Sean Fletcher
# Database Systems Assignment 01
# Sept 13, 2023

import os
import csv
from bs4 import BeautifulSoup
from DB_Ass01_functions import*


# the folder path of the folder the contains all the .html files
folder_path = r'C:\Users\fletc\PycharmProjects\DB\Ass_01\01'

# a list of all the html file names
html_file_names = os.listdir(folder_path)

# this is where the data from the html files will be stored before being written to a TSV file
all_the_data = []

# this is to set the labels for writing the information into a TSV file
all_the_data.append(
    ['file_name', 'paper_title', 'author_names', 'author_emails', 'author_affiliation', 'paper_abstract', 'keywords']
)

# grabbing each file and searching for the desired data
for i in range(len(html_file_names)):
    current_file = html_file_names[i]
    file_path = os.path.join(folder_path, current_file)
    with open(file_path, 'r', encoding='utf-8') as file:
        file_data = []
        html_content = file.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        # function calls on the html data parsed by Beautiful Soup
        title = find_the_title(soup)
        author_information = find_the_author_s(soup)  # this returns a triple
        author_names = author_information[0]  # triple[0]
        author_emails = author_information[1]  # triple[1]
        author_affiliations = author_information[2]  # triple[2]
        abstract = find_the_abstract(soup)
        keywords = generate_keywords(abstract)

        # appending the data to the file_data list
        file_data.append(current_file)
        file_data.append(title)
        file_data.append(author_names)
        file_data.append(author_emails)
        file_data.append(author_affiliations)
        file_data.append(abstract)
        file_data.append(keywords)

        # appending the file_data list to the larger data list all_the_data
        all_the_data.append(file_data)


# the name of the TSV file you wish to write
file_path = 'seans_tsv_file.tsv'

# Write data to the TSV file
with open(file_path, 'w', newline='', encoding='utf-8') as tsvfile:
    tsv_writer = csv.writer(tsvfile, delimiter='\t')
    for row in all_the_data:
        tsv_writer.writerow(row)
