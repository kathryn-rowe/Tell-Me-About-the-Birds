# Tell Me About the Birds

We're constantly surrounded by birds, and as they migrate, the frequency of sightings fluctuates. If we can better understand where birds spend most of their time, we can take steps to protect these key locations. 

"Tell Me About the Birds" is a visualization tool that allows users to explore data from the largest citizen-science dataset in the world ([eBird]) to better understand where birds have been sighted, when they are most abundant in various locations, and which other species may be present.

# Tech stack
Backend: Python, Flask, PostgreSQL, SQLAlchemy
Frontend: Javascript, jQuery, AJAX, JSON, Jinja, HTML5, CSS, Bootstrap, D3
APIs: Mapbox, DuckDuckGo

## Features
Homepage: choose a county and species
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Homepage")
Data page: explore eBird data! See where people saw this species and how many; investigate other species recorded at that location; choose another county and species.
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Data Page")

### Setup/Installation

Install requirements to run locally.

Clone repository:

```sh
$ git clone https://github.com/kathryn-rowe/Tell-Me-About-the-Birds.git
```
Create virtual environment:

```sh
$ virtualenv env
```
Activate virtual environment:
```sh
$ source env/bin/activate
```
Install dependencies:
```sh
$ pip install -r requirements.txt
```
Gather necessary secret keys from Mapbox and Flask. Save to your secrets file. Link to server.py.

Create database 'ebird_data'
```sh
$ createdb ebird_data
```
Create tables and seed example data running seed.py. Be sure to uncomment final lines in seed.py.
```sh
$ python seed.py
```
If you want to use SQLAlchemy to query the database, run in interactive mode
```sh
$ python -i model.py
```

### Todos

 - Write MOAR Tests
 - Add Night Mode

License
----

MIT


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [ebird]: <http://ebird.org/content/ebird/>

