WITH ratings AS (
SELECT * FROM {{ ref('fct_ratings') }}
),

tags AS (
SELECT * FROM {{ ref('src_tags') }}
),

all_users AS (
SELECT DISTINCT user_id FROM ratings
UNION
SELECT DISTINCT user_id FROM tags
)

SELECT
{{ dbt_utils.generate_surrogate_key(['u.user_id']) }} AS user_sk,
u.user_id,
-- statistics about user activity
COUNT(DISTINCT r.movie_id) AS total_movies_rated,
ROUND(AVG(r.rating), 2) AS avg_rating_given,
MIN(r.rating_timestamp) AS first_rating_date,
MAX(r.rating_timestamp) AS last_rating_date,
COUNT(DISTINCT t.tag) AS total_tags_applied
FROM all_users u
LEFT JOIN ratings r ON u.user_id = r.user_id
LEFT JOIN tags t ON u.user_id = t.user_id
GROUP BY u.user_id