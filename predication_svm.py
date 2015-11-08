import csv
import logger
import pandas as pd
import numpy as np
from sklearn import svm


input_file_path = "./data/sets/0/test.csv"
target_userid = 'AJRFZ0VZ0LD26'
# input from find_similar_users, K similar uid with similarities. THIS IS A FAKE INPUT just for testing
input_similarity = {"AJRFZ0VZ0LD26":0.7,"AZYJ9TS07B02W":0.78,"A1R602SXNGOMJ4":0.6,"A100JCBNALJFAW":0.8}

def estimateRatings(similar_user_list, similarity_list, table):
    # input_similarity's key is review_userid, value is similarity
    # first get convert to a list of similar users and their similarities

    logger.info('Starting to estimate ratings for the user...')
    # dot product to sum up the ratings for indivual product, then divide by sum of similarities
    # eg. we have ratings from three users for four moives, utility matrix is [[1, 0, 0, 4],[5, 1, 0, 3],[0, 0, 4, 1]]
    # similarity with target_user is [0.3, 0.7, 0.9]
    # then estimated_ratings for the first movie is (1x0.3 + 5x0.7)/(0.3 + 0.7) = 3.8
    similarity_array = np.array(similarity_list)
    similar_user_matrix = table.ix[similar_user_list].values
    estimated_ratings = np.dot(similarity_array, similar_user_matrix)

    divide_list = []
    for i in range(len(estimated_ratings)):
        sum_to_divide = 0
        for j in range(len(similar_user_matrix)):
            if similar_user_matrix[j][i] != 0:
                sum_to_divide += similarity_array[j]
            divide_list.append(sum_to_divide)
    for i in range(len(estimated_ratings)):
        if divide_list[i] != 0:
            estimated_ratings[i] = estimated_ratings [i] / divide_list[i]

    target_user_rating = table.ix[target_userid]
    clf = svm.SVR()
    clf.fit(table.ix[similar_user_list], similarity_list)
    # print clf.predict(target_user_rating)
    return estimated_ratings

similar_user_list = []
similarity_list = []
for key in input_similarity.iterkeys():
    similar_user_list.append(key)
for values in input_similarity.itervalues():
    similarity_list.append(values)

# read in data and pivot the table to be a matrix
logger.info('Redaing csv...')
df = pd.read_csv(input_file_path)

# find what products similar users have rated
df_similar_users = df[df.review_userid.isin(similar_user_list)]
table = pd.pivot_table(df_similar_users, values='review_score', index=['review_userid'], columns=['product_productid']).fillna(0)

estimated_ratings = estimateRatings(similar_user_list, similarity_list, table)

logger.info('Done processing')
for idx in range(len(estimated_ratings)):
    logger.info('Result product ' + table.columns[idx] + ' has rating: ' + str(estimated_ratings[idx]))