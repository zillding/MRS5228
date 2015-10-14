import csv

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

f = open("movie_reviews.csv", "wb")
w = csv.writer(f)
w.writerow(cols) # write table header first

def write_row(doc):
    w.writerow([doc.get(col) for col in cols])

count = 0
doc = {}
for line in open("./movies.txt"):
    line = line.strip()
    if line == "":
        write_row(doc)
        doc = {}
        count += 1
        if count % 100000 == 0:
            print "Number of records processed:", count
    else:
        idx = line.find(":")
        key, value = tuple([line[:idx], line[idx+1:]])
        key = key.strip().replace("/", "_").lower()
        value = value.strip()
        doc[key] = value
if doc:
    write_row(doc) # write the last row if there is one
    count += 1
print "Total number of records:", count
f.close()
