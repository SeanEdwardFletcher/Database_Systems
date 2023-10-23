import sqlite3


def enter_authors(cursor, lname, fname):
    # Check if the author already exists (optional)
    cursor.execute("SELECT * FROM Authors WHERE lname = ? AND fname = ?", (lname, fname))
    existing_author = cursor.fetchone()

    if existing_author is None:
        cursor.execute("INSERT INTO Authors (lname, fname) VALUES (?, ?)", (lname, fname))
    else:
        pass


def enter_papers(cursor, paper_id, title, last_updated, sub_by_lname, sub_by_fname):
    cursor.execute("INSERT INTO Papers (paper_id, title, last_updated, submitted_by_lname, submitted_by_fname) VALUES (?, ?, ?, ?, ?)",
                   (paper_id, title, last_updated, sub_by_lname, sub_by_fname))


def enter_paperauthors(cursor, paper_id, lname, fname):

    cursor.execute("SELECT paper_id, lname, fname FROM PaperAuthors WHERE paper_id = ? AND lname = ? AND fname = ?",
                   (paper_id, lname, fname))
    existing_record = cursor.fetchone()

    # If the query didn't return any results, insert the record
    if existing_record is None:
        cursor.execute(
            "INSERT INTO PaperAuthors (paper_id, lname, fname) VALUES (?, ?, ?)",
            (paper_id, lname, fname))
    else:
        pass


def enter_citations(cursor, citing_paper_id, cited_paper_id):

    # Check if the citation already exists
    cursor.execute(
        "SELECT citing_paper_id, cited_paper_id FROM Citations WHERE citing_paper_id = ? AND cited_paper_id = ?",
        (citing_paper_id, cited_paper_id))
    existing_citation = cursor.fetchone()

    # If the query didn't return any results, insert the citation
    if existing_citation is None:
        cursor.execute("INSERT INTO Citations (citing_paper_id, cited_paper_id) VALUES (?, ?)",
                       (citing_paper_id, cited_paper_id))
    else:
        pass


def enter_categories(cursor, category_name):
    # Check if the category already exists in the "Categories" table
    cursor.execute("SELECT category_name FROM Categories WHERE category_name = ?", (category_name,))
    existing_category = cursor.fetchone()

    if existing_category is None:
        # Insert the category into the "Categories" table
        cursor.execute("INSERT INTO Categories (category_name) VALUES (?)",
                       (category_name,))
    else:
        pass


def enter_papercategories(cursor, paper_id, category_name):
    cursor.execute("INSERT INTO PaperCategories (paper_id, category_name) VALUES (?, ?)",
                   (paper_id, category_name))

