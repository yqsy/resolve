import csv

import argparse

from collections import OrderedDict

PARSER = argparse.ArgumentParser()

PARSER.add_argument('csvfile', nargs=1, help='which csv file to be converted'
                                             'to sql')

PARSER.add_argument('--tacode', dest='tacode', action='store', required=True)

PARSER.add_argument('--filetype', dest='filetype', action='store', required=True)


def sql_generator(filename, tacode, filetype):
    with open(filename, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        for row_dict in reader:
            sorted_row = OrderedDict(sorted(row_dict.items(),
                                            key=lambda item: reader.fieldnames.index(item[0])))

            insert_str = '''INSERT INTO dbo.TFILEBACKMAP (FTACODE, FFLTYPE, FFLNAME, FBKNAME, FSPECIA)
VALUES ('{FTACODE}', '{FFLTYPE}', '{FFLNAME}', '{FBKNAME}', '')
GO

'''
            for key, value in sorted_row.items():
                sorted_row[key] = value.strip()

            yield insert_str.format(FTACODE=tacode, FFLTYPE=filetype,
                                    FFLNAME=sorted_row['field'], FBKNAME=sorted_row['back_field'])


def main():
    options = PARSER.parse_args()
    filename = options.csvfile[0]

    sql_func = sql_generator(filename, options.tacode, options.filetype)

    out_file_name = '{}-{}-TFILEBACKMAP.sql'.format(options.tacode, options.filetype)
    with open(out_file_name, 'w') as out_file:
        for sql_str in sql_func:
            out_file.write(sql_str)

    print(out_file_name, ' created')


if __name__ == '__main__':
    main()
