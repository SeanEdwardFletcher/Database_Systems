SELECT COUNT(DISTINCT pa.lname || pa.fname) - 1 AS num_authors
FROM PaperAuthors pa
WHERE pa.paper_id IN (
    SELECT paper_id
    FROM PaperAuthors
    WHERE (lname, fname) = ('Wei', 'Wu')
);