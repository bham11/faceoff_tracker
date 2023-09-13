SELECT 
    Player, 
{%- for field in additional_fields %}
    {{field}},
{%- endfor %}
    CAST(count(result) FILTER(WHERE Result = "W") AS varchar) || "/" || CAST(count(result) AS varchar) AS "FO%"
FROM {{team}}
{%- if filters|length > 0 %}
WHERE
{%- for filter in filters %}
    {{filter}}
{{- " AND" if not loop.last else "" }}
{%- endfor %}
{%- endif %}
GROUP BY
{%- if group_bys|length > 0 %}
Player,
{%- for groupby in group_bys %}
    {{groupby}}
{{- ","if not loop.last else "" }}
{%- endfor %}
{%- else %}
Player
{%-endif %}
ORDER BY 
Player;
