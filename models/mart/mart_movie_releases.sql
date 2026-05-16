{{ config(materialized = 'table') }}

WITH movies AS (
SELECT * FROM {{ ref('dim_movies') }}
),

ratings AS (
SELECT * FROM {{ ref('fct_ratings') }}
)

SELECT
m.release_year,
COUNT(DISTINCT m.movie_id) AS movies_released,
ROUND(AVG(r.rating), 2) AS avg_rating_that_year,
COUNT(r.user_id) AS total_ratings
FROM movies m
LEFT JOIN ratings r ON m.movie_id = r.movie_id
WHERE m.release_year IS NOT NULL
GROUP BY m.release_year
ORDER BY m.release_year