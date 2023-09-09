# Data extraction from ARXIV (https://arxiv.org/; https://ar5iv.org/)

In this assignment we were provided with a zip folder of 2,748 downloaded academic articles from ar5iv.org in .html format.

The goal was to extract the papers' titles, author(s) information (including names, affiliations, emails), abstract, and keywords.

All the extracted information must then be saved in .tsv file(s)

## Table of Contents

- [Installation](#Installation)
- [Usage](#Usage)
- [Results](#Results)
- [Conclusion](#Conclusion)

## Installation

To run this notebook, you will need to install the following libraries:

  os
  csv
  re
  BeautifulSoup
  yake
    
## Usage

- Download a collection of academic articles in .html format from (https://arxiv.org/; https://ar5iv.org/) 
- Add that folder's path to line 12 in DB_Ass01_Main
- Add a new file path to line 58 of DB_Ass01_Main (the name of the .tsv file you will be creating)
- run DB_Ass01_Main

## Results

Much of the data seems to have been cleanly extracted. There are, however, some anomalies such as: 

  some of the http files do not use the same div or class tags the majority of the other files use, and their information is there therefore missing
  
  some of the math papers use a form of notation in their abstracts that was not "cleaned" by BeautifulSoup, 
  the "dirty" abstract then bled into the keyword extraction and "dirtied" the keywords. example: "end_POSTSUBSCRIPT blackboard_A start_POSTSUBSCRIPT 3"

  some of the author information is mixed up with each other, like an email address of an author is sometimes included in the authors' affiliations section

There are probably more anomalies, but these are ones that I have found so far.

## Conclusion

Overall I feel that these python files do a fairly good job considering the variance in the html files. It was a fun exercise and I feel that I learned a lot.


