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

    test_userid_array = test_df.review_userid.unique()
    logger.info('Number of users in test data: %d' % len(test_userid_array))

    square_errors_array = []
    for target_userid in test_userid_array:
        # check whether this user id exists
        if not target_userid in train_df.review_userid.unique():
            logger.critical('Cannot find user in data with id: ' + target_userid)
            continue

        # compute similarity between this user and all others
        logger.debug('Computing similarity for user: ' + target_userid)

        # get users with which have common reviewed products
        # instead of looping through all other users
        # to improve performance
        common_products = train_df[train_df.review_userid == target_userid].product_productid
        userid_array = train_df[train_df.product_productid.isin(common_products)].review_userid.unique()
        logger.debug('Number of compared users: %d' % len(userid_array))

        result_sim = pd.Series()
        for index, userid in enumerate(userid_array):
            df = train_df[train_df.review_userid.isin([target_userid, userid])]
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

            if index > 0 and index % 500 == 0:
                logger.debug('Number of users processed: %d' % index)

        # drop the target user
        result_sim = result_sim.drop(target_userid)
        logger.debug('Done computing similarity')

        if not result_sim.any():
            logger.critical('Cannot find similar users for target user: ' + target_userid)
            continue

        for productid in test_df[test_df.review_userid == target_userid].product_productid.unique():
            logger.debug('Guessing rating for product: ' + productid)

            # find knn for this product
            rated_users = train_df[train_df.product_productid == productid].review_userid.unique()
            knn = result_sim.get(rated_users).sort_values(ascending=False)[:k].fillna(0)

            if not knn.any():
                logger.critical('Cannot find similar users for product: ' + productid)
                continue

            # predict the rating
            sim_weights = knn / knn.sum()
            product_df = train_df[train_df.product_productid == productid].groupby('review_userid').mean()
            user_ratings = product_df.loc[knn.index].review_score

            predict_rating = sim_weights.dot(user_ratings)

            # error control, set a boundary for error
            if predict_rating < 1: predict_rating = 1
            if predict_rating > 5: predict_rating = 5

            # compute error
            actual_rating = test_df[(test_df.product_productid == productid) & (test_df.review_userid == target_userid)].review_score.values[0]
            logger.debug('For product %s, predict rating: %f, actual rating: %f' % (productid, predict_rating, actual_rating))
            square_errors_array.append(np.square(predict_rating - actual_rating))

            logger.info('So far, root mean square error: %f' % np.sqrt(np.mean(square_errors_array)))

    # compute final error result
    rms_error = np.sqrt(np.mean(square_errors_array))
    logger.info('Root mean square error: %f' % rms_error)
    logger.debug('======================================')
