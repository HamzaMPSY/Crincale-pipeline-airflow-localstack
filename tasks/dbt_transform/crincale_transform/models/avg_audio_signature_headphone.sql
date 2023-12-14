WITH mapped_ranks AS (
    SELECT
        *
    FROM
        {{ ref("stg_maprankvalues") }}
),
final AS (
    SELECT
    headphone.signature,
    AVG(mapped_ranks.rank_value) AS average_rating,
    COUNT(headphone.signature) AS number_of_products
FROM
    `crincale-pipeline-gcp.crincale.crincale-headphones` headphone inner join mapped_ranks on headphone.rank = mapped_ranks.rank_grade
GROUP BY
    headphone.signature
HAVING
    COUNT(headphone.signature) > 15
)
SELECT
    *
FROM
    final