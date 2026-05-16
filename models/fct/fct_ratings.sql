{{
  config(
    materialized = 'incremental',
    on_schema_change='fail'
  )
}}

WITH src_ratings AS (
  SELECT * FROM {{ ref('src_ratings') }}
)

SELECT
  -- Surrogate key: unique identifier for each rating row
  {{ dbt_utils.generate_surrogate_key(['user_id', 'movie_id', 'rating_timestamp']) }} AS rating_sk,
  
  user_id,
  movie_id,
  rating,
  rating_timestamp
FROM src_ratings
WHERE rating IS NOT NULL

{% if is_incremental() %}
  -- الجزء المسؤول عن التحميل التراكمي: يجلب البيانات الجديدة فقط
  AND rating_timestamp > (SELECT MAX(rating_timestamp) FROM {{ this }})
{% endif %}