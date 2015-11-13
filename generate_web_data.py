import pandas as pd
import numpy as np
from scipy import spatial
import json

import logger

output_file_path = 'web-app/src/data.js'
max_compared_item = 200
max_sim_item = 10

################################################################################
# self defined helper functions
################################################################################
# compute centered cosine similarity
# between two pandas.Series
def calc_sim(s1, s2):
    def get_norm(s):
        return (s - s.mean()).fillna(0)

    norm_s1 = get_norm(s1)
    norm_s2 = get_norm(s2)

    if norm_s1.dot(norm_s2) == 0:
        result = 0
    else:
        result = 1 - spatial.distance.cosine(norm_s1, norm_s2)
    return result
################################################################################
# end of functions
################################################################################

logger.info('Start program: ' + __file__)

logger.debug('======================================')

data_file = 'data/movie_reviews.csv'
logger.info('Data file: ' + data_file)

logger.info('Start loading data...')
data_df = pd.read_csv(data_file)
logger.info('Done loading')

################################################################################
# user-user
complete_userid_array = data_df.review_userid.unique()
logger.info('Number of users in data: %d' % len(complete_userid_array))

user_sim_result = []
for target_userid in complete_userid_array:
    logger.debug('Computing similarity for user: ' + target_userid)

    # get users with which have common reviewed products
    # instead of looping through all other users
    # to improve performance
    common_products = data_df[data_df.review_userid == target_userid].product_productid
    userid_array = data_df[data_df.product_productid.isin(common_products)].review_userid.unique()
    logger.debug('Number of compared users: %d' % len(userid_array))
    if len(userid_array) > max_compared_item:
        logger.debug('Too many. Skip')
        continue

    result_sim = pd.Series()
    for index, userid in enumerate(userid_array):
        df = data_df[data_df.review_userid.isin([target_userid, userid])]
        # convert to pivot table to simplify calculation
        table = pd.pivot_table(
            df,
            values='review_score',
            index=['product_productid'],
            columns=['review_userid']
        )

        # calculate the similarity and store the result
        similarity = calc_sim(table[target_userid], table[userid])
        result_sim.set_value(userid, similarity)

    # drop the target user
    result_sim = result_sim.drop(target_userid).sort_values(ascending=False)
    if len(result_sim) > max_sim_item:
        result_sim = result_sim[:10]
    logger.debug('Done computing similarity')

    user_sim_result.append({
        'id': target_userid,
        'sim': json.loads(result_sim.to_json())
    })

    if len(user_sim_result) > 10:
        break

logger.info('Done computing user sim!')
logger.debug('======================================')

################################################################################
# item-item
complete_productid_array = data_df.product_productid.unique()
logger.info('Number of products in data: %d' % len(complete_productid_array))

item_sim_result = []
for target_productid in complete_productid_array:
    logger.debug('Computing similarity for product: ' + target_productid)

    # get products with which have common reviewers
    # instead of looping through all other products
    # to improve performance
    common_reviewers = data_df[data_df.product_productid == target_productid].review_userid
    productid_array = data_df[data_df.review_userid.isin(common_reviewers)].product_productid.unique()
    logger.debug('Number of compared products: %d' % len(productid_array))
    if len(productid_array) > max_compared_item:
        logger.debug('Too many. Skip')
        continue

    result_sim = pd.Series()
    for index, productid in enumerate(productid_array):
        df = data_df[data_df.product_productid.isin([target_productid, productid])]
        # convert to pivot table to simplify calculation
        table = pd.pivot_table(
            df,
            values='review_score',
            index=['review_userid'],
            columns=['product_productid']
        )

        # calculate the similarity and store the result
        similarity = calc_sim(table[target_productid], table[productid])
        result_sim.set_value(productid, similarity)

    # drop the target product
    result_sim = result_sim.drop(target_productid).sort_values(ascending=False)
    if len(result_sim) > max_sim_item:
        result_sim = result_sim[:10]
    logger.debug('Done computing similarity')

    item_sim_result.append({
        'id': target_productid,
        'sim': json.loads(result_sim.to_json())
    })

    if len(item_sim_result) > 10:
        break

logger.info('Done computing item sim!')

################################################################################
# write to file
logger.info('Write to file: ' + output_file_path)

output_file = open(output_file_path, 'wb')
output_file.write('// generated by ' + __file__)
output_file.write('\n')
output_file.close()
output_file = open(output_file_path, 'ab')
# user-user
output_file.write('// user-user\n')
output_file.write('export const userData =\n')
output_file.write(json.dumps(user_sim_result))
output_file.write('\n')
# item-item
output_file.write('// item-item\n')
output_file.write('export const itemData =\n')
output_file.write(json.dumps(item_sim_result))
output_file.write('\n')
output_file.close()

logger.info('Finish! Exit')
