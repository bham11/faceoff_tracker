SELECT Player, 
period,
CAST(count(result) FILTER(WHERE Result = "W") AS varchar) || "/" || CAST(count(result) AS varchar) AS "FO%"
FROM BC
GROUP BY
Player,
period
ORDER BY
period