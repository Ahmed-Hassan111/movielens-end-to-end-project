WITH src_movies AS (
    SELECT * FROM {{ ref('src_movies') }}
)
SELECT
    -- (Surrogate Key)
    {{ dbt_utils.generate_surrogate_key(['movie_id']) }} AS movie_sk,
    -- BK
    movie_id,
    
    --  تنظيف العنوان وحذف السنة منه (مثال: 'Toy Story (1995)' تصبح 'Toy Story')
    REGEXP_REPLACE(
        INITCAP(TRIM(title)),
        '\\s*\\(\\d{4}\\)$',
        ''
    ) AS movie_title,

    -- استخراج السنة كـ Integer
    TRY_CAST(REGEXP_SUBSTR(title, '\\d{4}', 1, 1) AS INT) AS release_year,

    SPLIT(genres, '|') AS genre_array,
    genres
FROM src_movies