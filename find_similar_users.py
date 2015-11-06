import pandas as pd
from scipy import spatial
import logger

input_file_path = 'data/sample.csv'
target_userid = 'A141HP4LYPWMSR'
k = 5

logger.info('Input file: ' + input_file_path)
logger.info('Target user id: ' + target_userid)
logger.info('Number of nearest kneighbor: %d' % k)

# read in data
logger.info('Start loading data...')
df = pd.read_csv(input_file_path)
table = pd.pivot_table(df, values='review_score', index=['product_productid'], columns=['review_userid']).fillna(0)
logger.info('Done loading!')

target_user_rating = table[target_userid]
# compute similarity between two vectors
def calc_sim(rating):
    # compute cosine similarity between target_user_rating and rating
    result = 1 - spatial.distance.cosine(target_user_rating, rating)
    return result

result = table.apply(calc_sim).drop(target_userid).sort_values(ascending=False)[:k]

logger.info('Done processing')
logger.info('Result: ' + result.to_json())
