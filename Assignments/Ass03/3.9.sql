SELECT lname, fname
FROM Authors
WHERE (lname, fname) IN (
    SELECT pa.lname, pa.fname
    FROM PaperAuthors pa
    GROUP BY pa.lname, pa.fname
    HAVING COUNT(*) = 1
);