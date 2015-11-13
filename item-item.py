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
################################################################################
# end of functions
################################################################################

logger.info('Start program: ' + __file__)
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
        for index, productid in enumerate(productid_array):
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

            if index > 0 and index % 500 == 0:
                logger.debug('Number of products processed: %d' % index)

        # drop the target product
        result_sim = result_sim.drop(target_productid)
        logger.debug('Done computing similarity')

        # no need to computer error if cannot find any similar items for this
        # product
        if not result_sim.any():
            logger.critical('Cannot find similar items for product: ' + target_productid)
            continue

        for userid in test_df[test_df.product_productid == target_productid].review_userid.unique():
            logger.debug('Guessing rating for user: ' + userid)

            # find knn for this user
            rated_items = train_df[train_df.review_userid == userid].product_productid.unique()
            knn = result_sim.get(rated_items).sort_values(ascending=False)[:k].fillna(0)

            if not knn.any():
                logger.critical('Cannot find similar items for user: ' + userid)
                continue

            # predict the rating
            sim_weights = knn / knn.sum()
            user_df = train_df[train_df.review_userid == userid].groupby('product_productid').mean()
            user_ratings = user_df.loc[knn.index].review_score

            predict_rating = sim_weights.dot(user_ratings)

            # error control, set a boundary for error
            if predict_rating < 1: predict_rating = 1
            if predict_rating > 5: predict_rating = 5

            # compute error
            actual_rating = test_df[(test_df.product_productid == target_productid) & (test_df.review_userid == userid)].review_score.values[0]
            logger.debug('For user %s, predict rating: %f, actual rating: %f' % (userid, predict_rating, actual_rating))
            square_errors_array.append(np.square(predict_rating - actual_rating))

            logger.info('So far, root mean square error: %f' % np.sqrt(np.mean(square_errors_array)))

    # compute final error result
    rms_error = np.sqrt(np.mean(square_errors_array))
    logger.info('Root mean square error: %f' % rms_error)
    logger.debug('======================================')
