SELECT title, homepage, year, acronym
FROM event_wikidata
WHERE eventInSeriesId == "$VARIABLE1$"
ORDER BY year DESC, homepage ASC, title ASC, acronym ASC;
