import pandas as pd
import numpy as np
from scipy import spatial

import logger

number_of_data_sets = 10
data_sets_dir = 'data/sets/'
k = 5

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

# get one user ratings for a variaties of product in knn
def get_user_ratings(user_df, knn):
    s = pd.Series(data=user_df.review_score.values, index=user_df.product_productid)
    return s.loc[knn.index]
################################################################################
# end of functions
################################################################################

logger.info('Start program...')
logger.info('Number of data sets: %d' % number_of_data_sets)
logger.info('Data sets dir: ' + data_sets_dir)
logger.info('Number of nearest neighbors: %d' % k)

logger.debug('======================================')

# loop throught data sets
for i in range(number_of_data_sets):
    test_file = data_sets_dir + str(i) + '/test.csv'
    train_file = data_sets_dir + str(i) + '/train.csv'
    # load test and train data
    logger.info('Test data file: ' + test_file)
    logger.info('Train data file: ' + train_file)

    logger.info('Start loading data...')
    test_df = pd.read_csv(test_file)
    train_df = pd.read_csv(train_file)
    logger.info('Done loading')

    test_productid_array = test_df.product_productid.unique()
    logger.info('Number of products in test data: %d' % len(test_productid_array))

    square_errors_array = []
    for target_productid in test_productid_array:
        # check whether this product id exists
        if not target_productid in train_df.product_productid.unique():
            logger.critical('Cannot find product in data with id: ' + target_productid)
            continue

        # compute similarity between this product and all others
        logger.debug('Computing similarity for product: ' + target_productid)

        # get products with which have common reviewers
        # instead of looping through all other products
        # to improve performance
        common_reviewers = train_df[train_df.product_productid == target_productid].review_userid
        productid_array = train_df[train_df.review_userid.isin(common_reviewers)].product_productid.unique()
        logger.debug('Number of compared products: %d' % len(productid_array))

        result_sim = pd.Series()
        for productid in productid_array:
            df = train_df[train_df.product_productid.isin([target_productid, productid])]
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
        result_sim = result_sim.drop(target_productid)
        logger.debug('Done computing similarity')

        for userid in test_df[test_df.product_productid == target_productid].review_userid.unique():
            # find knn for this user
            rated_items = train_df[train_df.review_userid == userid].product_productid.unique()
            knn = result_sim.get(rated_items).sort_values(ascending=False)[:k]
            logger.debug('For user ' + userid + ', knn: ' + knn.to_string())

            # predict the rating
            sim_weights = knn / knn.sum()
            user_df = train_df[train_df.review_userid == userid]
            user_ratings = get_user_ratings(user_df, knn)

            predict_rating = sim_weights.dot(user_ratings)

            # compute error
            actual_rating = test_df[(test_df.product_productid == target_productid) & (test_df.review_userid == userid)].review_score.values[0]
            square_errors_array.append(np.square(predict_rating - actual_rating))

    # compute final error result
    rms_error = np.sqrt(np.mean(square_errors_array))
    logger.info('Root mean square error: %f' % rms_error)
    logger.debug('======================================')
