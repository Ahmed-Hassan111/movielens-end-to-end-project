-- Bridge table: resolves many-to-many between dim_movies and dim_genome_tags

WITH src_scores AS (
SELECT * FROM {{ ref('src_genome_score') }}
)
SELECT
movie_id,
tag_id,
ROUND(relevance, 4) AS relevance_score
FROM src_scores
WHERE relevance > 0 -- استبعاد العلاقات الضعيفة جداً أو المعدومة لتوفير مساحة التخزين وتسريع الأداء