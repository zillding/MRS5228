import csv
import logger
import pandas as pd
import numpy as np
from sklearn import svm


input_file_path = "./data/sets/0/test.csv"

def estimateRatings(input_similarity, ot):
    # input_similarity's key is review_userid, value is similarity
    # first get convert to a list of similar users and their similarities
    similar_user_list = []
    similarity_list = []
    for key in input_similarity.iterkeys():
        similar_user_list.append(key)
    for values in input_similarity.itervalues():
        similarity_list.append(values)

    logger.info('Starting to estimate ratings for the user...')
    # dot product to sum up the ratings for indivual product, then divide by sum of similarities
    similarity_array = np.array(similarity_list)
    S = np.dot(similarity_array, ot.ix[similar_user_list].values)
    estimated_ratings = S/sum(similarity_list)

    return estimated_ratings

# input from find_similar_users, K similar uid with similarities. THIS IS A FAKE INPUT just for testing
#input_similarity = {"A3Q4S5DFVPB70D":0.1, "A1J50B4K22D93F":0.4}
input_similarity = {"AJRFZ0VZ0LD26":0.0055555556,"AZYJ9TS07B02W":0.0055555556,"A1R602SXNGOMJ4":0.0055555556,"A100JCBNALJFAW":0.0055555556}

# read in data and pivot the table to be a matrix
df = pd.read_csv(input_file_path, nrows=10000)
logger.info('Redaing csv...')

logger.info('Start to convert to pivot table...')
ot = pd.pivot_table(df, values='review_score', index=['review_userid'], columns=['product_productid']).fillna(0)

estimated_ratings = estimateRatings(input_similarity, ot)
nonzero_idx = np.nonzero(estimated_ratings)[0]

logger.info('Done processing')
for idx in nonzero_idx:
	logger.info('Result product ' + ot.columns[idx] + ' has rating: ' + str(estimated_ratings[idx]))