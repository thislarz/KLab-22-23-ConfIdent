| SeriesId    | title                                                                | entries | hasUrlPattern | title conf |
|-------------|----------------------------------------------------------------------|---------|---------------|------------|
| Q6053150    | The *th International Semantic Web Conference                        | 84      | yes           | yes        |
| Q1961016    | Neural Information Processing Systems *                              | 38      | yes           | yes        |
| Q3570023    | The Web Conference *                                                 | 31      | mostly        | yes        |
| Q17012957   | ESWC *                                                               | 21      | yes           | yes        |
| Q18353514   | The * Conference on Empirical Methods in Natural Language Processing | 54      | mostly        | yes        |


---

### 07.12.2022 SimpleEventPredictor

Events:  2061

Events not null:  1947

Successes:  17

Success rate:  0.8731381612737545 %

---
### simpleEventPredictor examples (03.02.2023)

Q17012957 prediction success

Q18353514 prediction success

Q3570023 prediction fail

Q1961016 prediction success

Q6053150 prediction fail

---
### mgep (03.02.2023)

#### 1

Event(title='Conference on Artificial Intelligence', year=2016, acronym='AAAI 2016', homepage='http://www.aaai.org/Conferences/AAAI/aaai16.php', series_id='') last

Event(title='Conference on Artificial Intelligence', year='2017', acronym='AAAI 2017', homepage='http://www.aaai.org/Conferences/AAAI/aaai17.php', series_id='') next

403 Forbidden  :  -1 (title : str.find())

False

#### 2

Last event of: AAL 2008 "Acquisition of African Languages" has taken place in year 2008

Next event of: AAL 2008 "Acquisition of African Languages" takes place in the year 2009

False

//should update all years in title