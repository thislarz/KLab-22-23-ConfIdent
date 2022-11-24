SELECT title, homepage, year, acronym
FROM event_wikidata
    WHERE eventInSeriesId IS '<var2>'
ORDER BY year DESC