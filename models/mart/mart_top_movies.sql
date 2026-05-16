{{ config(materialized = 'table') }}

WITH ratings AS (
SELECT * FROM {{ ref('fct_ratings') }}
),

movies AS (
SELECT * FROM {{ ref('dim_movies') }}
),

aggregated AS (
SELECT
r.movie_id,
m.movie_title,
m.release_year,
m.genres,
COUNT(r.user_id) AS rating_count,
ROUND(AVG(r.rating), 2) AS avg_rating
FROM ratings r
LEFT JOIN movies m ON r.movie_id = m.movie_id
GROUP BY r.movie_id, m.movie_title, m.release_year, m.genres
)

SELECT *
FROM aggregated
WHERE rating_count >= 50 -- only statistically meaningful movies
ORDER BY avg_rating DESC, rating_count DESC