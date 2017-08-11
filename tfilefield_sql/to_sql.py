import csv

import argparse
import re

from collections import OrderedDict

PARSER = argparse.ArgumentParser()

PARSER.add_argument('csvfile', nargs=1, help='which csv file to be converted'
                                             'to sql')

PARSER.add_argument('--tacode', dest='tacode', action='store', required=True)

PARSER.add_argument('--filetype', dest='filetype', action='store', required=True)


def get_type(field_type):
    """获取字段类型"""
    field_map = {'C': '0', 'A': '0', 'N': '2'}

    if field_type not in field_map.keys():
        return field_map['C']

    return field_map[field_type]


def get_integer_length(length):
    """获取长度,如果有小数信息,剔除掉"""
    if not '(' in length:
        return length

    regex = r".+(?=\()"

    rtn = re.search(regex, length)

    return rtn.group()


def get_decimal_digit(length):
    """获取小数长度"""
    digital_map = {'一': '1', "两": '2', "二": '2', "三": '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9',
                   '十': '10'}

    if not '(' in length:
        return '0'

    regex = r"(?<=\().+(?=位)"

    rtn = re.search(regex, length)

    if not rtn:
        return length

    return digital_map[rtn.group()]


def get_alignment(alg_type):
    """获取对齐方式"""
    alignment_map = {'C': '1', 'A': '1', 'N': '34'}

    if alg_type not in alignment_map.keys():
        return alignment_map['C']

    return alignment_map[alg_type]


def add_generator():
    i = -1
    while True:
        i = i + 1
        yield i


def sql_generator(filename, tacode, filetype):
    add_func = add_generator()

    with open(filename, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        # way 1 to print dict in an order
        # for row in reader:
        #     print(['{}: {}'.format(k, row[k]) for k in reader.fieldnames])

        for row_dict in reader:
            sorted_row = OrderedDict(sorted(row_dict.items(),
                                            key=lambda item: reader.fieldnames.index(item[0])))

            insert_str = '''INSERT INTO dbo.TFILEFIELD (FTACODE, FFLTYPE, FFINAME, FFITYPE, FFILENG, FFISUBL, FFIALGN, FFIORDR, FFIIDEN, FFIDNEED, FFDEFAULT)
VALUES ('{FTACODE}', '{FFLTYPE}', '{FFINAME}', {FFITYPE}, {FFILENG}, {FFISUBL}, {FFIALGN}, {FFIORDR}, '{FFIIDEN}', 'Y', NULL)
GO

'''
            for key, value in sorted_row.items():
                sorted_row[key] = value.strip()

            yield insert_str.format(FTACODE=tacode, FFLTYPE=filetype,
                                    FFINAME=sorted_row['字段名'], FFITYPE=get_type(sorted_row['类型']),
                                    FFILENG=get_integer_length(sorted_row['长度']),
                                    FFISUBL=get_decimal_digit(sorted_row['长度']),
                                    FFIALGN=get_alignment(sorted_row['类型']), FFIORDR=next(add_func),
                                    FFIIDEN=sorted_row['ID'])


def main():
    options = PARSER.parse_args()
    filename = options.csvfile[0]

    sql_func = sql_generator(filename, options.tacode, options.filetype)

    out_file_name = '{}-{}-TFILEFIELD.sql'.format(options.tacode, options.filetype)
    with open(out_file_name, 'w') as out_file:
        for sql_str in sql_func:
            out_file.write(sql_str)

    print(out_file_name, ' created')


if __name__ == '__main__':
    main()
