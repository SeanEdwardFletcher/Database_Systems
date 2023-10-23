SELECT Papers.title
FROM Papers
JOIN PaperAuthors ON Papers.paper_id = PaperAuthors.paper_id
WHERE PaperAuthors.lname = "Eto" AND PaperAuthors.fname = "Minoru"
ORDER BY Papers.last_updated DESC;