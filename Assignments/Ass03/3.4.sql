SELECT Papers.title
    FROM Papers
    WHERE Papers.paper_id NOT IN (
        SELECT DISTINCT citing_paper_id
        FROM Citations
    )