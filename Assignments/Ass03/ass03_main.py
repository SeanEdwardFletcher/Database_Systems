import json
from build_db import *
from populate_the_db import *
from tqdm import tqdm

name_your_database = "seans_test_database.db"  # don't forget to add a ".db" at the end of the database name

build_the_db(name_your_database)

# if you are writing csv file make sure to set encoding
with open('arXiv21.json', 'r', encoding="utf-8") as json_file:

    conn13 = sqlite3.connect(name_your_database)
    cursor = conn13.cursor()

    for line in tqdm(json_file):

        # information for an individual paper
        paper = json.loads(line)

        # inserting an instance into the Papers table
        paper_id = float(paper['id'])
        title = paper['title']
        last_update = paper['last_update']
        submitter = paper['submitter']
        sub_names = submitter.split()
        sub_last_name = sub_names[0]
        sub_first_name = " ".join(sub_names[1:]) # I'm NOT separating the first and middle names out because Shea told
                                                 # me there were authors with the same first and last name, but
                                                 # different middle names
        enter_papers(cursor, paper_id, title, last_update, sub_last_name, sub_first_name)

        # inserting instances into the Authors and PaperAuthors tables
        lst_author = paper['authors']
        for name in lst_author:
            names = name.split()
            last_name = names[0]
            first_name = " ".join(names[1:])  # I'm NOT separating the first and middle names out because Shea told me
                                              # there were authors with the same first and last name, but different middle names
            enter_authors(cursor, last_name, first_name)
            enter_paperauthors(cursor, paper_id, last_name, first_name)

        # inserting instances into Categories and PaperCategories tables
        categories = paper['categories']  # cs.LG cs.AI
        individual_categories = categories.split()
        for cat in individual_categories:
            enter_categories(cursor, cat)
            enter_papercategories(cursor, paper_id, cat)

        # inserting instances into the Citations table
        cited = paper['cited']  # ['2104.11956', '2112.05638', '2105.09406', '2110.02823', '2109.08587']
        lst_cited = eval(cited)
        for citation in lst_cited:
            enter_citations(cursor, paper_id, float(citation))

        conn13.commit()

    conn13.close()
