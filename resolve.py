import csv

if __name__ == '__main__':
    with open('03_example.csv', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)

