-- Create a temporary table to store the rankings
CREATE TEMPORARY TABLE band_rankings AS
SELECT origin, SUM(nb_fans) AS total_fans
FROM metal_bands
GROUP BY origin;

-- Rank the origins based on the total number of fans
SET @rank = 0;
SELECT @rank := @rank + 1 AS rank, origin, total_fans
FROM band_rankings
ORDER BY total_fans DESC;

-- Clean up the temporary table
DROP TEMPORARY TABLE band_rankings;

