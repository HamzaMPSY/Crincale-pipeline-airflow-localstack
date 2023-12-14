WITH mapped_ranks AS (
    SELECT
        *
    FROM
        {{ ref("stg_maprankvalues") }}
),
final AS (
    SELECT
        iems.signature,
        AVG(mapped_ranks.rank_value) AS average_rating,
        COUNT(iems.signature) AS number_of_products
    FROM
        `crincale-pipeline-gcp.crincale.crincale-iems` iems inner join 
        mapped_ranks on  iems.rank = mapped_ranks.rank_grade
    GROUP BY
        iems.signature
    HAVING
        COUNT(iems.signature) > 35
)
SELECT
    *
FROM
    final