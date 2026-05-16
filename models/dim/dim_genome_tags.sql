WITH src_tags AS (
    SELECT * FROM {{ ref('src_genome_tags') }}
)
SELECT
    -- (Surrogate Key)
    {{ dbt_utils.generate_surrogate_key(['tag_id']) }} AS tag_sk,
    
    tag_id,
    INITCAP(TRIM(tag)) AS tag_name
FROM src_tags