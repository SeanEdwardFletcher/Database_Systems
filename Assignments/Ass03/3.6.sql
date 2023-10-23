    SELECT Categories.category_name, COUNT(PaperCategories.paper_id) AS num_papers_in_category
    FROM Categories
    LEFT JOIN PaperCategories ON Categories.category_name = PaperCategories.category_name
    GROUP BY Categories.category_name
    ORDER BY num_papers_in_category DESC;