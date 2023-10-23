    SELECT COUNT(*) AS num_papers
    FROM (
        SELECT P.paper_id
        FROM Papers P
        JOIN PaperAuthors PA ON P.paper_id = PA.paper_id
        WHERE PA.lname = 'Sengupta' AND PA.fname = 'Indranath'
        AND P.paper_id IN (
            SELECT paper_id
            FROM PaperAuthors
            GROUP BY paper_id
            HAVING COUNT(*) <= 2
        )
    );