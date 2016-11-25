# RecipeGenerator
This is a project for the Big Data Analytics course at Columbia.

Data are scaped from Allrecipes.com (http://allrecipes.com/recipes/?grouping=all). Each row contains the following features:
  1. id: ID of the recipe (type: string)
  2. made_it_count: the number of users who have tried the recipe (type: int)
  3. time: the total time needed for the recipe (including preparing and cooking) (type: int)
  4. direction: cooking instructions (type: string)
  5. ingredients: a list of ingredients needed for the recipe (type: list)

To use the scraper, you need to first download:
  1. MongoDB: 
      (i). in terminal: 
      brew install mongodb 
      (make sure homebrew is installed first)
      (ii). start mongodb: 
      Linux: brew services start mongodb
      Windows: http://stackoverflow.com/questions/20796714/what-is-the-way-to-start-mongo-db-from-windows-7-64-bit
  2. Chromedriver (if you are using Chrome):
      https://chromedriver.storage.googleapis.com/index.html?path=2.25/
  3. Install the following python libraries:
      selenium, pymongo, numpy, pandas
        
After everything is installed, run the python script allrecipe.py and you are all set!

