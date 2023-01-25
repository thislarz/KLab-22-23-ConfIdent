SELECT title, homepage, year, acronym
FROM $VARIABLE1$
WHERE homepage IS NOT NULL
    AND
    (
$VARIABLE_YEARS$
    )
ORDER BY year DESC, homepage ASC, title ASC, acronym ASC;