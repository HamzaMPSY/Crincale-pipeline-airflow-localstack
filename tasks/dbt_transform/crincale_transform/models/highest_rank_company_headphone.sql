WITH mapped_ranks AS (
    SELECT
        *
    FROM
        {{ ref("stg_maprankvalues") }}
),
company AS (
    SELECT
        *
    FROM
        {{ ref("stg_companynames") }}
),
final AS (
    SELECT
        company.company_name,
        AVG(mapped_ranks.rank_value) AS average_rating,
        COUNT(company.company_name) AS number_of_products
    FROM
        `crincale-pipeline-gcp.crincale.crincale-headphones` headphone 
        inner join mapped_ranks on headphone.rank = mapped_ranks.rank_grade
        inner join company on company.company_name = {{ dbt.split_part(
            string_text = 'headphone.model',
            delimiter_text = "' '",
            part_number = 1
        ) }}
    GROUP BY
        company.company_name
)
SELECT
    *
FROM
    final