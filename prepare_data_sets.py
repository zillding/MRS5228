import os
import logger

n = 10
input_file_path = './data/movie_reviews.csv'
output_dir = './data/sets/'

logger.info('Number of data sets: %d' % n)
logger.info('Input file: ' + input_file_path)
logger.info('Output dir: ' + output_dir)

input_file = open(input_file_path, 'rb')

# prepare output files
output = []
for i in range(n):
    # create the output dir if it does not exist
    dirname = output_dir + `i`
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    dict = {
        'train': open(dirname + '/train.csv', 'wb'),
        'test': open(dirname + '/test.csv', 'wb')
    };
    output.append(dict)

# process data and write to output
count = 0
for line in input_file:
    count += 1

    if count == 1:
        # write header to every file
        for dict in output:
            dict['train'].write(line)
            dict['test'].write(line)
        continue

    # determine where should this line go
    test_index = count % n
    for index, dict in enumerate(output):
        if index == test_index:
            dict['test'].write(line)
        else:
            dict['train'].write(line)

    if count % 100000 == 1:
        logger.debug('Number of records processed: %d' % count-1)

logger.info('Number of lines processed: %d' % count)

# close files
input_file.close()
for dict in output:
    dict['train'].close()
    dict['test'].close()
