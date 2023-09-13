SELECT 
    Player, 
{%- for field in additional_fields %}
    {{field}},
{%- endfor %}
    CAST(count(result) FILTER(WHERE Result = "W") AS varchar) || "/" || CAST(count(result) AS varchar) AS "FO%"
FROM {{team}}
GROUP BY
{%- if filters|length > 0 %}
Player,
{%- for filter in filters %}
    {{filter}}
{{- " AND" if not loop.last else ";" }}
{%- endfor %}
{%- else %}
Player
{{-";"}}
{%-endif %}

-- SELECT 
--     Player, 
--     CAST(count(result) FILTER(WHERE Result = "W") AS varchar) || "/" || CAST(count(result) AS varchar) AS "FO%"
-- FROM BU
-- GROUP BY Player