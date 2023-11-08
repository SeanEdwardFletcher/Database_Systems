import mysql.connector
import json
import time

config_file = "connectorConfig.json"


# Methods
# Method 01
def releaseyearCount():
    # connecting to the db using the credentials in the json file
    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]
    data_base = mysql.connector.connect(**connection_config)

    # creating my cursor
    cursor = data_base.cursor()

    # my MySQL query
    # it counts series, AND orders them, by release year
    query = """
    SELECT ReleaseYear, COUNT(*) 
    FROM tvSeries 
    WHERE ReleaseYear IS NOT NULL 
    GROUP BY ReleaseYear 
    ORDER BY ReleaseYear;
    """

    # call the query
    cursor.execute(query)

    # these are the results
    result = cursor.fetchall()

    # Close up shop
    cursor.close()
    data_base.close()

    return result


# Methods 02 and 03
def getSeries(star_name, genre=None):
    if genre == None:
        # connecting to the db using the credentials in the json file
        with open(config_file, "r") as f:
            config = json.load(f)
        connection_config = config["mysql"]
        data_base = mysql.connector.connect(**connection_config)

        # creating my cursor
        cursor = data_base.cursor()

        # my MySQL query
        # getting the titles of everything the 'star' was in
        query = """
        SELECT DISTINCT s.Title
        FROM tvSeries AS s
        JOIN SeriesStars AS ss ON s.IMDB_id = ss.IMDB_id
        WHERE ss.star = %s;
        """

        # call the query; the star's name is the parameter
        cursor.execute(query, (star_name,))

        # get the results into a list; it's a list of tuples in the cursor
        result = [row[0] for row in cursor.fetchall()]

        # Close up shop
        cursor.close()
        data_base.close()

        return result

    else:

        with open(config_file, "r") as f:
            config = json.load(f)
        connection_config = config["mysql"]
        data_base = mysql.connector.connect(**connection_config)

        # creating my cursor
        cursor = data_base.cursor()

        # the SQL query
        # it gets the titles and ratings of a series using genre and star
        query = """
        SELECT DISTINCT s.Title, s.Rating
        FROM tvSeries AS s
        JOIN SeriesStars AS ss ON s.IMDB_id = ss.IMDB_id
        JOIN SeriesGenre AS sg ON s.IMDB_id = sg.IMDB_id
        WHERE ss.star = %s AND sg.Genre = %s;
        """

        # call it; the star's name and the genre are the parameters
        cursor.execute(query, (star_name, genre))

        # get the results; it's a list of tuples [("series name", Decimal(the rating)),]
        results = cursor.fetchall()

        # print(results[:5])

        if results:
            print(f"Series featuring {star_name} in the {genre} genre:")
            for title, rating in results:
                print(f"Title: {title}, Rating: {rating}")
        else:
            print(f"No series found for {star_name} in the {genre} genre.")

        # Close up shop
        cursor.close()
        data_base.close()


# Method 04
def getSeriesCostar(star_names):
    # checking the input here, no funny business please
    if len(star_names) < 2 or len(star_names) > 10:
        return "Please provide a list of 2 to 10 star names."

    # connecting to the db using the credentials in the json file
    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]
    data_base = mysql.connector.connect(**connection_config)

    # creating my cursor
    cursor = data_base.cursor()

    # Build the query dynamically to join each star
    query = """
    SELECT DISTINCT s.Title
    FROM tvSeries AS s
    """

    join_clause = ""
    where_clause = ""

    for i in range(len(star_names)):
        join_clause += f"""
        JOIN SeriesStars AS ss{i + 1} ON s.IMDB_id = ss{i + 1}.IMDB_id
        """

        where_clause += f"AND ss{i + 1}.star = %s\n"

    query += join_clause
    query += "WHERE 1 "  # To start the WHERE clause
    query += where_clause

    # do the query
    # a list of star names is the parameter
    cursor.execute(query, star_names)

    # the results os a list of titles in tuples
    results = cursor.fetchall()
    # I just want the titles in their own list
    to_return = [x[0] for x in results]

    # Closing up shop
    cursor.close()
    data_base.close()

    return to_return


# Method 05
def getPopularSeries(star_name):
    # connecting to the db using the credentials in the json file
    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]
    data_base = mysql.connector.connect(**connection_config)

    # creating my cursor
    cursor = data_base.cursor()

    # the SQL query
    # it gets the series titles where that series' rating is higher than the average rating
    query = """
    SELECT s.Title
    FROM tvSeries AS s
    JOIN SeriesStars AS ss ON s.IMDB_id = ss.IMDB_id
    WHERE ss.star = %s
      AND s.Rating > (SELECT AVG(Rating) FROM tvSeries)
    """

    cursor.execute(query, (star_name,))
    result = cursor.fetchall()  # a list of tuples

    # close up shop
    cursor.close()
    data_base.close()

    # turn the list of tuples into a list of strings
    popular_series = [row[0] for row in result]

    return popular_series


# Method 06
def getRatingPerGenre():
    # connecting to the db using the credentials in the json file
    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]
    data_base = mysql.connector.connect(**connection_config)

    # creating my cursor
    cursor = data_base.cursor()

    # the SQL query
    # it calculates the average rating for each genre
    query = """
    SELECT sg.Genre, AVG(s.Rating) AS AverageRating
    FROM SeriesGenre AS sg
    JOIN tvSeries AS s ON sg.IMDB_id = s.IMDB_id
    GROUP BY sg.Genre
    """

    # call it
    cursor.execute(query)

    # Behrooz wants it printed in the method for some reason
    print("Genre\t\tAverage Rating")
    print("---------------------------")
    for genre, avg_rating in cursor:
        print(f"{genre}\t\t{avg_rating:.2f}")

    # Close up shop
    cursor.close()
    data_base.close()


# Method 07
def getSeriesDirectorStarGenre(director, star, genre):
    # connecting to the db using the credentials in the json file
    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]
    data_base = mysql.connector.connect(**connection_config)

    # creating my cursor
    cursor = data_base.cursor()

    # the SQL query
    # it gets titles that meet the 3 criteria: director, star, genre
    query = """
    SELECT s.Title
    FROM tvSeries AS s
    JOIN SeriesDirector AS sd ON s.IMDB_id = sd.IMDB_id
    JOIN SeriesStars AS ss ON s.IMDB_id = ss.IMDB_id
    JOIN SeriesGenre AS sg ON s.IMDB_id = sg.IMDB_id
    WHERE sd.director = %s
      AND ss.star = %s
      AND sg.Genre = %s
    """

    # call it
    cursor.execute(query, (director, star, genre))
    result = cursor.fetchall()  # a list of tuples

    # Close the cursor and the database connection
    cursor.close()
    data_base.close()

    # turning the list of tuples into a list of strings
    series_titles = [row[0] for row in result]

    return series_titles


# Functions and Procedures
# 01
def createAvgFunction():
    # connecting to the db using the credentials in the json file
    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]
    data_base = mysql.connector.connect(**connection_config)

    # creating a cursor
    cursor = data_base.cursor()

    # just making sure it doesn't already exist... I was getting errors that I couldn't interpret
    drop_function_query = "DROP FUNCTION IF EXISTS GetAverageRatingsPerGenre;"
    cursor.execute(drop_function_query)

    # the SQL function;
    # this creates the function in the database.
    # the function calculates the average rating per genre
    avg_function_query = """
CREATE FUNCTION GetAverageRatingsPerGenre() 
RETURNS MEDIUMTEXT -- Use MEDIUMTEXT for larger JSON data
BEGIN
    DECLARE result MEDIUMTEXT;

    SELECT JSON_ARRAYAGG(
        JSON_OBJECT(Genre, AverageRating)
    ) INTO result
    FROM (
        SELECT sg.Genre, AVG(s.Rating) AS AverageRating
        FROM SeriesGenre AS sg
        JOIN tvSeries AS s ON sg.IMDB_id = s.IMDB_id
        GROUP BY sg.Genre
    ) subquery;

    RETURN result;
END;"""
    # Execute the SQL function creation query
    cursor.execute(avg_function_query)

    # Committing the changes to the database
    data_base.commit()

    # Close up shop
    cursor.close()
    data_base.close()


def callAvgFunction():
    # connecting to the db using the credentials in the json file
    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]

    # Connect to the database
    data_base = mysql.connector.connect(**connection_config)
    cursor = data_base.cursor()

    # Call the function stored in the DB
    cursor.execute("SELECT GetAverageRatingsPerGenre()")

    # get the result
    result = cursor.fetchall()

    if result:
        # The result is a tuple, so extract the value from it
        return result[0][0]
    else:
        print("Function didn't return a result")

    cursor.close()
    data_base.close()


def pythonAvgFunction():
    # connecting to the db using the credentials in the json file
    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]
    data_base = mysql.connector.connect(**connection_config)

    # creating my cursor
    cursor = data_base.cursor()

    # Retrieve genres and ratings from the database
    query = """
    SELECT sg.Genre, s.Rating
    FROM SeriesGenre AS sg
    JOIN tvSeries AS s ON sg.IMDB_id = s.IMDB_id
    """
    cursor.execute(query)

    # Create a dictionary to store ratings for each genre
    genre_ratings = {}

    for genre, rating in cursor:
        if genre not in genre_ratings:
            genre_ratings[genre] = [rating]
        else:
            genre_ratings[genre].append(rating)

    # Calculate the average ratings for each genre
    average_ratings = {}
    for genre, ratings in genre_ratings.items():
        average_rating = sum(ratings) / len(ratings)
        average_ratings[genre] = average_rating

    # Close the cursor and the database connection
    cursor.close()
    data_base.close()

    return average_ratings


def createProcedure():
    # connecting to the db using the credentials in the json file
    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]
    data_base = mysql.connector.connect(**connection_config)

    # creating a cursor
    cursor = data_base.cursor()

    # the SQL script for dropping the procedure if it already exists
    drop_procedure_sql = "DROP PROCEDURE IF EXISTS UpdateSeriesRating"

    # the SQL script for the new procedure
    # it updates the rating of a series using the series IMDB_id
    create_procedure_sql = """
    CREATE PROCEDURE UpdateSeriesRating(IN imdbID VARCHAR(10), IN newRating DECIMAL(3, 1))
BEGIN
    IF newRating >= 0 AND newRating <= 10 THEN
        UPDATE tvSeries
        SET Rating = newRating
        WHERE IMDB_id = imdbID;
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid rating. The rating must be between 0 and 10.';
    END IF;
END;

    """

    try:
        # Drop the procedure if it exists
        cursor.execute(drop_procedure_sql)

        # Execute the SQL script to create the new procedure
        cursor.execute(create_procedure_sql)

        # Commit the changes to the database
        data_base.commit()
        print("Stored procedure created successfully")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close up shop
        cursor.close()
        data_base.close()


def updateRating(imdb_id, new_rating):
    # connecting to the db using the credentials in the json file
    with open(config_file, "r") as f:
        config = json.load(f)
    connection_config = config["mysql"]
    data_base = mysql.connector.connect(**connection_config)

    # creating a cursor
    cursor = data_base.cursor()

    try:
        # Call the procedure
        cursor.callproc("UpdateSeriesRating", (imdb_id, new_rating))
        # Commit the changes
        data_base.commit()
        print(f"Rating for IMDb ID: {imdb_id} is now {new_rating}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        data_base.close()


list_01 = ["Angelina Jolie", "Brad Pitt"]
list_02 = ['Keanu Reeves', 'Laurence Fishburne', 'George Georgiou', 'Lance Reddick']
list_03 = ['Conrad Kemp', 'Forest Whitaker', 'Inge Beckmann', 'Orlando Bloom']
list_04 = ['Clancy Brown', 'Laura Bailey']
list_05 = ['Ewan McGregor', 'Hayden Christensen', 'Natalie Portman']
list_06 = ['Carrie-Anne Moss', 'Hugo Weaving', 'Keanu Reeves', 'Laurence Fishburne']
list_07 = ['Documentary', 'Animation', 'Sci-Fi']
list_08 = ['Lana Wachowski', 'Keanu Reeves', 'Sci-Fi']
lst_lst = [list_01, list_02, list_03, list_04, list_05, list_06]


if __name__ == "__main__":
    print(" ")
    print(" ")

    # printing the results from Method 01
    print("********************")
    print("Method 1 results:")
    print(releaseyearCount())
    print("********************")
    print(" ")
    print(" ")
    print(" ")
    print(" ")

    # printing the results from Method 02
    print("********************")
    print("Method 2 results:")
    print(" ")
    for name in list_01:
        print(f"{name} has starred in:")
        print(getSeries(name))
        print(" ")
    print("********************")
    print(" ")
    print(" ")
    print(" ")
    print(" ")

    # printing the results from Method 03
    print("********************")
    print("Method 3 results:")
    print(" ")
    for name in list_01:
        for gen in list_07:
            getSeries(name, gen)
            print(" ")
    print("********************")
    print(" ")
    print(" ")
    print(" ")
    print(" ")

    # printing the results from Method 04
    print("********************")
    print("Method 4 results:")
    print(" ")
    names_concat = ""
    for name in list_01:
        names_concat += name + ", "
    print(names_concat[:-2] + " have starred together in:")
    print(getSeriesCostar(list_01))
    print(" ")
    names_concat = ""
    for name in list_05:
        names_concat += name + ", "
    print(names_concat[:-2] + " have starred together in:")
    print(getSeriesCostar(list_05))
    print(" ")
    print("********************")
    print(" ")
    print(" ")
    print(" ")
    print(" ")

    # printing the results from Method 05
    print("********************")
    print("Method 5 results:")
    print(" ")
    for name in list_05:
        print(f"{name} starred in these popular series:")
        print(getPopularSeries(name))
        print(" ")
    print("********************")
    print(" ")
    print(" ")
    print(" ")
    print(" ")

    # printing the results from Method 06
    print("********************")
    print("Method 6 results:")
    print(" ")
    getRatingPerGenre()
    print("********************")
    print(" ")
    print(" ")
    print(" ")
    print(" ")

    # printing the results from Method 07
    print("********************")
    print("Method 7 results:")
    print(" ")
    print(f"{list_08[2]} series staring {list_08[1]} where {list_08[0]} directed:")
    print(getSeriesDirectorStarGenre(list_08[0], list_08[1], list_08[2]))
    print(" ")
    print("********************")
    print(" ")
    print(" ")
    print(" ")
    print(" ")

    # Printing the results from Functions and Procedures 01
    print("********************")
    print("Functions and Procedures 01 results:")
    print(" ")
    # creating the function in the database
    createAvgFunction()
    # Record the start time
    start_time_01 = time.time()
    callAvgFunction()
    end_time_01 = time.time()
    start_time_02 = time.time()
    pythonAvgFunction()
    end_time_02 = time.time()
    # Calculate the elapsed times
    elapsed_time_01 = end_time_01 - start_time_01
    elapsed_time_02 = end_time_02 - start_time_02
    print(f"The SQL function took {elapsed_time_01:.4f} seconds to run.")
    print(f"The Python function took {elapsed_time_02:.4f} seconds to run.")
    print(" ")
    print("********************")
    print(" ")
    print(" ")
    print(" ")
    print(" ")
    """
    ('World War Z', 'tt0816711'), ('Mr. & Mrs. Smith', 'tt0356910'),
    ('Eternals', 'tt9032400'), ('Gone in 60 Seconds', 'tt0187078'),
    """
    print("********************")
    print("Functions and Procedures 02 results:")
    print(" ")
    # creating the procedure in the DB
    print("calling createProcedure()")
    createProcedure()
    print(" ")
    # calling the procedure wrapped in python code
    print("calling updateRating() with IMDB_id 'tt0816711' (World War Z) and rating 9.9:")
    updateRating('tt0816711', 9.9)
    print(" ")
    print("calling updateRating() with IMDB_id 'tt0187078' (Gone in 60 Seconds) and rating 11.1:")
    updateRating('tt0187078', 11.1)
    print(" ")
    print("********************")



