import requests
import json
import pprint
import pandas as pd
import sqlalchemy as db
response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
out = response.json()
first_story = out[0] # seems like latest story is first one
story = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{first_story}.json?print=pretty')
json_file = story.json()
title = json_file['title']
author = json_file['by']
link = json_file['url']
print(f'Title is "{title}."')
print(f'Author is {author}.')
print(f'Link is {link}.')


dataframe = pd.DataFrame.from_dict(out) # place all story records into a dataframe
engine = db.create_engine('sqlite:///stories.db')
dataframe.to_sql('records', con=engine, if_exists='replace', index=False)
with engine.connect() as connection:
   query_result = connection.execute(db.text("SELECT * FROM records;")).fetchall()
   print(pd.DataFrame(query_result))

