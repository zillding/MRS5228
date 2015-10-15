import os

n = 3
input_file_path = './data.csv'
output_dir = './data/'

input_file = open(input_file_path)

# prepare output files
output = []
for i in range(n):
    # create the output dir if it does not exist
    dirname = output_dir + `i+1`
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    dict = {
        'train': open(dirname + '/train.csv', 'w'),
        'test': open(dirname + '/test.csv', 'w')
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

print 'Number of lines processed:', count

# close files
input_file.close()
for dict in output:
    dict['train'].close()
    dict['test'].close()
