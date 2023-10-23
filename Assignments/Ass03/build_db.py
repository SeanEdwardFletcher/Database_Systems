import sqlite3


def build_the_db(data_base_title):

    conn = sqlite3.connect(data_base_title)

    cursor = conn.cursor()

    # Papers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Papers(
            paper_id REAL PRIMARY KEY, 
            title TEXT, 
            last_updated DATE, 
            submitted_by_lname TEXT,
            submitted_by_fname TEXT,
            FOREIGN KEY (submitted_by_lname, submitted_by_fname) REFERENCES Authors(lname, fname)
        )
    ''')

    # Authors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Authors( 
            fname TEXT, 
            lname TEXT,
            PRIMARY KEY (lname, fname)
        )
    ''')

    # PaperAuthors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PaperAuthors (
            paper_id REAL,
            lname TEXT,
            fname TEXT,
            PRIMARY KEY (paper_id, lname, fname),
            FOREIGN KEY (paper_id) REFERENCES Papers(paper_id),
            FOREIGN KEY (lname, fname) REFERENCES Authors(lname, fname)
        )
    ''')

    # Citations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Citations (
            citing_paper_id REAL,
            cited_paper_id REAL,
            PRIMARY KEY (citing_paper_id, cited_paper_id),
            FOREIGN KEY (citing_paper_id) REFERENCES Papers(paper_id),
            FOREIGN KEY (cited_paper_id) REFERENCES Papers(paper_id)
        )
    ''')

    # Categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            category_name TEXT PRIMARY KEY
        )
    ''')

    # PaperCategories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PaperCategories (
            paper_id REAL,
            category_name TEXT,
            PRIMARY KEY (paper_id, category_name),
            FOREIGN KEY (paper_id) REFERENCES Papers(paper_id),
            FOREIGN KEY (category_name) REFERENCES Categories(category_name)
        )
    ''')

    conn.commit()
    conn.close()

