{{ config(materialized = 'table') }}

WITH movies AS (
    SELECT * FROM {{ ref('dim_movies') }}
),

ratings AS (
    SELECT * FROM {{ ref('fct_ratings') }}
),


movie_genres AS (
    SELECT 
        m.movie_id,
        genre.value::STRING AS genre
    FROM movies m,
    LATERAL FLATTEN(input => m.genre_array) genre
    WHERE genre.value::STRING != '(no genres listed)'
)

SELECT
    mg.genre,
    COUNT(DISTINCT mg.movie_id) AS movie_count,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    COUNT(r.user_id) AS total_ratings
FROM movie_genres mg
LEFT JOIN ratings r ON mg.movie_id = r.movie_id
GROUP BY mg.genre
ORDER BY total_ratings DESC