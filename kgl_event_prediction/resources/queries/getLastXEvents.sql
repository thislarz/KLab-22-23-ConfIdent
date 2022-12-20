SELECT title, homepage, startDate, acronym
FROM $VARIABLE1$
WHERE homepage IS NOT NULL
    AND
    (startDate LIKE '202%' OR
     startDate LIKE '2019%' OR
     startDate LIKE '2018%')
ORDER BY startDate DESC, homepage ASC, title ASC, acronym ASC;