## How to Use this?
### *main.py*
The ``main.py`` file contains the code to run a query in python. I think it uses SQL-Lite but not sure on that one.

#### Usage
To use make sure the EventCorpus.db is at the right location (see important notes below)

If you want to run a query best practice is to create a new Query in the Queries Directory and change the path inside the ``main.py`` file accordingly.

> For further development it might be usefull to save the results to a file as well.
 

### *openDBinBrowser*
The ``openDBinBrowser.py`` is a wraper file to simply the process of accessing the database via browser.

#### Usage
To use only make sure the EventCorpus.db is at the right location (see important notes below).

### important Notes
The DataBase has to be named ``EventCorpus.db`` and needs to be located at this path ``$home$/.conferencecorpus/EventCorpus.db`` 
where ``$home$`` specifies your users directory. 
This usually this is ``C:/Users/steve``. 
In that directory you create a folder named ``.conferencecorpus`` and place the data-base there.

Example Path would be:
``C:/Users/steve/.conferencecorpus/EventCorpus.db``
