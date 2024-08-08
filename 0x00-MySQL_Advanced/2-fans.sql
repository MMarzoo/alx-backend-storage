-- Retrieves the total number of fans for each origin of metal bands, sorted in descending order.
SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;