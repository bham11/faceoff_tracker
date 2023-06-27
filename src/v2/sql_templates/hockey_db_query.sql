Select 
    * 
From {{table_name}}
{%- if filters|length > 0 %}
WHERE
{%- for filter in filters %}
    {{filter}}
{{- " AND" if not loop.last else ";" }}
{%- endfor %}
{%- else %}
{{-";"}}
{%-endif %}