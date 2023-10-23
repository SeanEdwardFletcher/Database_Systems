SELECT COUNT(DISTINCT c.citing_paper_id) AS num_papers_citing_lei_yin
    FROM Citations c
    WHERE c.cited_paper_id IN (
        SELECT pa.paper_id
        FROM PaperAuthors pa
        WHERE pa.lname = 'Yin' AND pa.fname = 'Lei'
    )