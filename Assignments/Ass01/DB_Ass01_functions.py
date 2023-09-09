import re
import yake


def generate_keywords(input_text):
    """
    This function uses YAKE to extract keywords from a scientific article's abstract.
    The abstract is provided as the "input_text" and the keywords are returned as a list of strings
    """

    # lan="en" means the language is set to english
    # n=2 means it will produce keywords of length 5 or less
    # deduplLim=0.9 means that is two keywords have a similarity score of 90% or higher, only one will be kept
    # dedupFunc='seqm' tells YAKE to use the sequence match deduplication function
    # top=5 means it is only going to grab the 5 best matches
    keyword_extractor = yake.KeywordExtractor(lan="en", n=2, dedupLim=0.9, dedupFunc='seqm', top=5)

    keywords = keyword_extractor.extract_keywords(input_text)
    keywords_to_return = []

    for keyword, score in keywords:
        keywords_to_return.append(keyword)

    return keywords_to_return


def find_the_author_s(the_soup):
    """
    This function uses Beautiful Soup to search through html text.
    It finds the author information using an html class tag and then
    feeds that text into a regex clearing function:
         clean_author_text_with_regex()
    it then cleans the information in the 'names' category
    and fills in empty categories with a "no information found" kind of string
    """

    # finding the author information using the class "ltx_authors"
    author_divs = the_soup.find_all('div', class_='ltx_authors')

    # Extract the text from each div and store it in a list
    author_divs_list = [div.get_text() for div in author_divs]
    # joining the list into one string for regex processing
    author_divs_text = ''.join(author_divs_list)

    # finding the pertinent data with regex
    names, emails, affiliations = clean_author_text_with_regex(author_divs_text)

    # cleaning the names
    names = [x.lstrip() for x in names]
    clean_names = [s.replace('&', '') for s in names]

    # if data seems to be missing....
    if len(names) == 0:
        clean_names.append("No author names were found.")
    if len(emails) == 0:
        emails.append("No author emails were found.")
    if len(affiliations) == 0:
        affiliations.append("No author affiliations were found.")

    return names, emails, affiliations


def clean_author_text_with_regex(input_text):

    """
    this function uses a series of regex searches to find and categorize information
    """

    # Initialize lists to store the data
    names = []
    emails = []
    affiliations = []

    # the regex patterns
    # building the name finding pattern
    two_name_pattern = r'(\S+\s+\S+)'
    three_name_pattern = r'(\S+\s+\S+\s+\S+)'
    two_names_or_three_names_pattern = r'(' + two_name_pattern + r'|' + three_name_pattern + r')'
    full_name_pattern = r'^(?!.*_)\s*(,)?\s*' + two_names_or_three_names_pattern + r'\s*$'  # possible commas, no underscores
    #
    email_pattern = r'\s*(\S+@\S+)\s*'
    #
    affiliation_pattern = r'^\s*(?:\S+\s+){3,}\S+\s*$'
    #
    # regex patterns for excluding matches
    number_pattern = r'\d'
    underscore_pattern = r'_'

    # Split the input text into lines
    lines = input_text.split('\n')

    # Iterate through the lines
    for line in lines:

        #using regex to find author names
        name_match = re.search(full_name_pattern, line)
        if name_match:
            possible_name_text = name_match.group()

            # if the match contains a number, don't use it
            number_match = re.search(number_pattern, possible_name_text)
            if number_match:
                pass

            # if there are no numbers in the match, it's probably a name
            else:
                names.append(name_match.group().strip())
            continue

        # finding the emails with regex
        email_match = re.search(email_pattern, line)
        if email_match:
            emails.append(email_match.group().strip())

        # finding the author affiliations with regex
        affiliation_match = re.search(affiliation_pattern, line)
        if affiliation_match:
            possible_affiliation_text = affiliation_match.group()

            # excluding all matches with underscores, this is because a few html tags with underscores were sneaking in
            underscore_match = re.search(underscore_pattern, possible_affiliation_text)
            if underscore_match:
                pass
            else:
                affiliations.append(affiliation_match.group().strip())
            continue

    return names, emails, affiliations


def find_the_title(the_soup):
    """
    This function uses Beautiful Soup to search through html text.
    It finds a 'title' element in the html and returns the title
    If no title was found it returns the string "Title not found"
    """
    title_element = the_soup.find('title')
    title = title_element.text if title_element else "Title not found"

    # A regex pattern to match square brackets and anything inside them
    pattern = r'\[.*?\]'

    # use regex to remove matches of the pattern
    title = re.sub(pattern, '', title)

    title = title.strip()

    return title


def find_the_abstract(the_soup):
    """
        This function uses Beautiful Soup to search through html text.
        It finds a 'ltx_abstract' class element in the html and returns the abstract text
        If no class element was found it returns the string "Abstract not found."
        """

    # Find the <div> element with class="ltx_abstract"
    abstract_div = the_soup.find('div', class_='ltx_abstract')

    # Getting the text content
    if abstract_div:
        abstract_text = abstract_div.get_text(strip=True)
        abstract_text = abstract_text[8:]
    else:
        abstract_text = "Abstract not found."

    return abstract_text
