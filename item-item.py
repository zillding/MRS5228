import pandas as pd
import numpy as np
from scipy import spatial

import logger

number_of_data_sets = 10
data_sets_dir = 'data/sets/'
k = 5

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

    logger.info('Start converting to pivot table')
    test_table = pd.pivot_table(
        test_df,
        values='review_score',
        index=['review_userid'],
        columns=['product_productid']
    )
    train_table = pd.pivot_table(
        train_df,
        values='review_score',
        index=['review_userid'],
        columns=['product_productid']
    )
    logger.info('Done converting to pivot table')

    # normalize data to use centered cosine similarity
    logger.info('Start normalizing data...')
    norm_train_table = (train_table - train_table.mean()).fillna(0)
    logger.info('Done normalizing.')

    def guess(series):
        productid = series.name

        if not productid in train_table:
            logger.critical('Cannot find product with id: ' + productid)
            return series.map(lambda x: np.nan)

        target_product_rating = norm_train_table[productid]
        # compute similarity between two vectors
        def calc_sim(rating):
            if (target_product_rating * rating).sum() == 0:
                result = 0
            else:
                # compute cosine similarity between target_user_rating and rating
                result = 1 - spatial.distance.cosine(target_user_rating, rating)
            return result

        logger.debug('Compute similarity of product: ' + productid)
        sim_series = norm_train_table.apply(calc_sim)

        # for each user guess the rating for this product
        result = []
        for (userid, rating) in series.iteritems():
            # get this user has rated items
            products_series = train_df[train_df.review_userid == userid].product_productid
            # get knn for this user
            knn = sim_series.drop(productid).get(products_series).sort_values(ascending=False)[:k]
            # compute similarity weights
            sim_weights = knn / knn.sum()
            # predict rating and add to result
            predict_rating = sim_weights.dot(train_table.loc[userid].get(products_series))
            result.append(predict_rating)

        return result;

    guess_result = test_table.apply(guess)
    logger.debug('Guess result: \n' + guess_result.to_string())

    # evaluate algo
    rms_error = np.sqrt(np.square(test_table - guess_result).stack().mean())

    logger.info('Root mean square error: %f' % rms_error)
    logger.debug('======================================')
