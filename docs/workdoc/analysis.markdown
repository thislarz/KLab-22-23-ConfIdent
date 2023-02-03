### event_wikidata analytics:

number of series: 2059

average series length: 3.57

series with homepages: 78 -> 3.79% //only checked first instance for homepage

series with 3 or less: 1386 -> 67.31%

series with 10 or more: 113 -> 5.49%

---

### event_wikidata analytics II (16.12.22):

#### event_wikidata

8026  : Total Number of Events

875  : Total Number of Events with Homepages - 10.902 % of Total

7558  : Total Number of Events with a linked Series - 94.169 % of Total

#### event_orclone

9016  : Total Number of Events

8653  : Total Number of Events with Homepages - 95.974 % of Total

5546  : Total Number of Events with a linked Series - 61.513 % of Total

#### event_or

8835  : Total Number of Events

8762  : Total Number of Events with Homepages - 99.174 % of Total

4867  : Total Number of Events with a linked Series - 55.088 % of Total

#### eventseries_orclone

956  : Total Number of Events

215  : Total Number of Events with Homepages - 22.49 % of Total

---
----------event_wikidata-------------

8026  : Total number of entries

875  : Total number of entries with Homepages - 10.902 % of Total

7558  : Total number of entries with a linked series - 94.169 % of Total

7396  : Total number of entries with a year - 92.151 % of Total

----------event_orclone-------------

9016  : Total number of entries

8653  : Total number of entries with Homepages - 95.974 % of Total

5546  : Total number of entries with a linked series - 61.513 % of Total

9260  : Total number of entries with a year - 102.706 % of Total

----------event_or-------------

8835  : Total number of entries

8762  : Total number of entries with Homepages - 99.174 % of Total

4867  : Total number of entries with a linked series - 55.088 % of Total

9092  : Total number of entries with a date - 102.909 % of Total

1  : Total number of entries with a year - 0.011 % of Total

----------eventseries_orclone-------------

956  : Total number of entries

215  : Total number of entries with Homepages - 22.49 % of Total

1126  : Total number of entries with a year - 117.782 % of Total

---

### event_or analytics (20.12.22)

#### dataquality of last 20 years (20.12.22)

7774  Events in last 20  years

47  fake homepages detected** 0.6 %

407  events have empty titles 5.24 %

<br/>

#### dataquality of last 15 years

7256  Events in last 15  years

28  fake homepages detected** 0.39 %

289  events have empty titles 3.98 %

<br/>

#### dataquality of last 10 years

4223  Events in last 10  years

10  fake homepages detected** 0.24 %

154  events have empty titles 3.65 %

<br/>

#### dataquality of last 5 years

2468  Events in last 5  years

5  fake homepages detected** 0.2 %

10  events have empty titles 0.41 %

<br/>

#### dataquality of last 2 years

843  Events in last 2  years

0  fake homepages detected** 0.0 %

0  events have empty titles 0.0 %

<br/>

#### methods
** hompages containing the following strings are considered to be fake:

["elsevier", "springer", "inderscience", "dblp", "wikicfp.com"]

Manuall controll of the 2022 entries suggests that the problem of unauthentic homepages, does not persist in new entries.

<br/>

#### conclusion

dataquality seems satisfactory on first analysis

---

### event_or analysis (20.12.22)

1964  Events in last 4  years

650  Acronyms occur at least twice

104  at least events have a written numeral in title. 1952 total events*

<br/>

843  Events in last 2  years

169  Acronyms occur at least twice

52  at least events have a written numeral in title. 843  total events

<br/>

#### conclusion

We seem to have 5% to 20% written numerals in the titles. Is annoying but okay to deal with.

---

### event_orclone analysis (19.01.23)

851  Events in last 3  years

9  fake homepages detected** 1.06 %

1  events have empty titles 0.12 %

316  Acronyms occur at least twice

45  at least events have a written numeral in title. 841  total events

<br/>

Since it is 2023 we have to look at last 3 years.

---

### event_orclone acronym matchings (19.01.23)

524  series count - 276  acronym not string - 841  total events - letzte 3 Jahre

1024  series count - 276  acronym not string - 1529  total events - letzte 4 Jahre

1105  series count - 276  acronym not string - 1991  total events - letzte 5 Jahre

1239  series count - 276  acronym not string - 2508  total events - letzte 6 Jahre

2152  series count - 279  acronym not string - 4053  total events - letzte 10 Jahre

#### conclusion

Apparently are most series short, meaning they only have one or two entries over a long timespan. As a consequence our 
algorithm should work on a single event entry and the main use of matching acronyms is to clean prediction data to not 
count doubles.

---

### event_or_clone column analysis (03.02.2023)

Methodology: This used SeriesAnalysis.count_column_in_table() which uses countSeriesVariable.sql to count entries.

5546 : in event_orclone in inEventSeries

9268 : in event_orclone in acronym

9268 : in event_orclone in lookupAcronym //probably same as above

1482 : in event_orclone in ordinal

9016 : in event_orclone in title

9260 : in event_orclone in year

9221 : in event_orclone in city //this can be a good confirmation tool with high confidence (but only for current event)

8653 : in event_orclone in homepage

246 : in event_orclone in wikidataId

---