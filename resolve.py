import csv

if __name__ == '__main__':
    with open('03_example.csv', encoding='utf-8-sig') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            print(','.join(row))
