import os
import logger

n = 20
input_file_path = './data/movie_reviews.csv'
output_dir = './data/sets/'

logger.info('Number of data sets: %d' % n)
logger.info('Input file: ' + input_file_path)
logger.info('Output dir: ' + output_dir)

input_file = open(input_file_path, 'rb')

# process data and write to output
count = 0
k = 1
headerline = ''
for line in input_file:
    count += 1

    # determine where should this line go
    test_index = count % n

    if count == 1:
        # write header to every file
        headerline = line;
        continue

    dirname = output_dir + `test_index`
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        dict = {
            'train': open(dirname + '/train.csv', 'wb'),
            'test': open(dirname + '/test.csv', 'wb'),
        };
        dict['train'].write(headerline)
        dict['test'].write(headerline)
    else:
        dict = {
            'train': open(dirname + '/train.csv', 'ab'),
            'test': open(dirname + '/test.csv', 'ab')
        };
    if(k>=n*n):
        dict['train'].write(line)
    else:
        dict['test'].write(line)

    if(k!=n*n+n):
        k=k+1
    else:
        k = 1
    if count % 100000 == 1:
        logger.debug('Number of records processed: %d' % (count-1))

logger.info('Number of lines processed: %d' % count)

# close files
input_file.close()
for dict in output:
    dict['train'].close()
    dict['test'].close()
