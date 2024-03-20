-- Lists all bands with 'Glam rock' as their main style, ranked by their longevity
SELECT name AS band_name, (2022 - IFNULL(split, 2022) + IFNULL(formed, 0)) AS lifespan
FROM bands
WHERE main_style = 'Glam rock'
ORDER BY lifespan DESC;
