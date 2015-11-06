import sys
sys.path.insert(0, '../')

import pandas as pd

input_file_path = '../data/sample.csv'

df = pd.read_csv(input_file_path)

print len(df.product_productid.unique())
print pd.pivot_table(df, values='review_score', index=['review_userid'], columns=['product_productid'])

# print df[df.review_userid=='A3Q4S5DFVPB70D'].product_productid.unique().size

# for userid in df.review_userid.unique():
#     number_of_movies_reviewed = df[df.review_userid==userid].product_productid.unique().size
#     if number_of_movies_reviewed > 1:
#         print userid, 'reviewed', number_of_movies_reviewed, 'movies'

