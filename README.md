Movie Recommendation System
===========================

NUS CS5228 Course Project

### Data source:

[SNAP](https://snap.stanford.edu/data/web-Movies.html)

[Download](https://snap.stanford.edu/data/movies.txt.gz)

### Get the project source code

`$ git clone https://github.com/ZillDing/MRS5228`

### Usage

+ Put the raw data file `movies.txt` in the dir `data`

+ Run `parse_to_csv.py` to parse the original txt data to csv format

  `$ python parse_to_csv.py`

+ Run `prepare_data_sets.py` to split the csv file to multiple training & testing data sets

  `$ python prepare_data_sets.py`

+ Run `item-item.py` or `user-user.py` to run the recommender and obtain error result. The result is both displayed on the console and written to log file.

  `$ python item-item.py` or `$ python user-user.py`

### Test Web App

+ Run `generate_web_data.py` to generate data for the web app

  `$ python generate_web_data.py`

+ Install dependancies (with node installed)

  `$ cd web-app && npm install`

+ Start the web app

  `$ npm start`

+ Open browser and point to [http://localhost:3000](http://localhost:3000)
