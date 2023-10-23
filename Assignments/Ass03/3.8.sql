    SELECT Papers.title
    FROM Papers
    WHERE Papers.paper_id NOT IN (
        SELECT paper_id
        FROM PaperAuthors
        GROUP BY paper_id
        HAVING COUNT(*) > 1
    );