import csv
import logger

input_file_path = './data/movies.txt'
output_file_path = './data/movie_reviews.csv'

logger.info('Input file: ' + input_file_path)
logger.info('Output file: ' + output_file_path)

input_file = open(input_file_path, 'rb')
cols = [
    'product_productid',
    'review_userid',
    'review_profilename',
    'review_helpfulness',
    'review_score',
    # 'review_time',
    # 'review_summary',
    # 'review_text'
    ]

output_file = open(output_file_path, 'wb')
w = csv.writer(output_file)
w.writerow(cols) # write table header first

def write_row(doc):
    w.writerow([doc.get(col) for col in cols])

count = 0
doc = {}
for line in input_file:
    line = line.strip()
    if line == '':
        write_row(doc)
        doc = {}
        count += 1
        if count % 100000 == 0:
            logger.debug('Number of records processed: %d' % count)
    else:
        idx = line.find(':')
        key, value = tuple([line[:idx], line[idx+1:]])
        key = key.strip().replace('/', '_').lower()
        value = value.strip()
        doc[key] = value

# write the last row if there is one
if doc:
    write_row(doc)
    count += 1

logger.info('Total number of records: %d' % count)

# close files
input_file.close()
output_file.close()
