# Tell Me About the Birds

We're constantly surrounded by birds, and as they migrate, the frequency of sightings fluctuates. If we can better understand where birds spend most of their time, we can take steps to protect these key locations. 

"Tell Me About the Birds" is a visualization tool that allows users to explore data from the largest citizen-science dataset in the world ([eBird]) to better understand where birds have been sighted, when they are most abundant in various locations, and which other species may be present.

# Tech stack
Backend: Python, Flask, PostgreSQL, SQLAlchemy

Frontend: Javascript, jQuery, AJAX, JSON, Jinja, HTML5, CSS, Bootstrap, D3

APIs: Mapbox, DuckDuckGo

## Features

Homepage: choose a county and species

![alt text](https://github.com/kathryn-rowe/Tell-Me-About-the-Birds/blob/master/static/images/_readme-img/homepage.jpg "Homepage")


Data page: explore eBird data! See where people saw this species and how many; investigate other species recorded at that location; choose another county and species.

![alt text](https://github.com/kathryn-rowe/Tell-Me-About-the-Birds/blob/master/static/images/_readme-img/data_page.jpg "Data Page")

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

Database
If you want to link the app to my database hosted on AWS --> contact me at kjrowe06@gmail.com.
```sh
#in model.py
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://kate_admin:thepassword@the-birds.cbec8qxdlxnj.us-west-1.rds.amazonaws.com:5432/the_birds"
```

If you want to create your own, local database --> 1. Create database 'ebird_data' 2. Use the example ebird data provided 3. Seed database with seed.py
```sh
$ createdb ebird_data
```
```sh
#in model.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ebird_data'
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

 - Write more tests
 - Include all CA counties
 - Grab bird by species type
 - Highlight chosen species on D3 graph

License
----

Copyright 2017 Kathryn Rowe

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [ebird]: <http://ebird.org/content/ebird/>

