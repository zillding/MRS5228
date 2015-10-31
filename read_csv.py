import pandas as pd

df = pd.read_csv("./data/sets/0/test.csv")

print df[df.review_userid=='A3Q4S5DFVPB70D'].product_productid.unique().size

for userid in df.review_userid.unique():
    number_of_movies_reviewed = df[df.review_userid==userid].product_productid.unique().size
    if number_of_movies_reviewed > 1:
        print userid, 'reviewed', number_of_movies_reviewed, 'movies'

