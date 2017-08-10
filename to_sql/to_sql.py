import csv

import argparse

from collections import OrderedDict

PARSER = argparse.ArgumentParser()

PARSER.add_argument('csvfile', metavar='csvfile', nargs=1, help='which csv file to be converted'
                                                                'to sql')


def main():
    options = PARSER.parse_args()

    filename = options.csvfile[0]

    with open(filename, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        # way 1 to print dict in an order
        # for row in reader:
        #     print(['{}: {}'.format(k, row[k]) for k in reader.fieldnames])

        for row_dict in reader:
            sorted_row = OrderedDict(sorted(row_dict.items(),
                                            key=lambda item: reader.fieldnames.index(item[0])))
            print(sorted_row)


if __name__ == '__main__':
    main()
