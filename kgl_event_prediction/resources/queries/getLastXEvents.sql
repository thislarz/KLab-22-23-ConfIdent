SELECT title, homepage, startDate, acronym
FROM $VARIABLE1$
WHERE homepage IS NOT NULL
    AND
    (
$VARIABLE_YEARS$
    )
ORDER BY startDate DESC, homepage ASC, title ASC, acronym ASC;