import csv

import copy
import argparse

PARSER = argparse.ArgumentParser()

PARSER.add_argument('-c', '--csv', action='store', dest='csvfile',
                    default=None, help='文件模板csv文件')

PARSER.add_argument('-t', '--txt', action='store', dest='txtfile',
                    default=None, help='基金文件')


def get_field_len(length_in_ch):
    """
    一般是数字,还有16(两位小数)这种情况,要转换成数字
    """
    if '(' not in length_in_ch:
        return int(length_in_ch)

    idx = length_in_ch.find('(')
    length = length_in_ch[:idx]
    return int(length)


if __name__ == '__main__':
    OPTIONS = PARSER.parse_args()

    if not OPTIONS.csvfile:
        PARSER.print_help()
        print('请输出-c')
        exit(-1)

    if not OPTIONS.txtfile:
        PARSER.print_help()
        print('请输出-t')
        exit(-1)

    stand_structure = []
    with open(OPTIONS.csvfile, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # 每一个字段的各种属性
            stand_structure.append(row)

    with open(OPTIONS.txtfile, encoding='utf-8') as f:
        lines = f.read().splitlines()

        file_field_nums = int(lines[9])
        if file_field_nums != len(stand_structure):
            print('字段数量不相等,文件标准字段数:{} 实际数量:{}'.format(
                len(stand_structure), file_field_nums))
            exit(-1)

        file_fields = lines[10:10 + file_field_nums]

        if len(file_fields) != file_field_nums:
            print('文件字段数量为:{},实际字段不满足该数量:{},字段:{}'.format(
                file_field_nums, len(file_fields), file_fields))
            exit(-1)

        for field, stand_field in zip(file_fields, stand_structure):
            if field != stand_field['字段名']:

                if field.lower() == stand_field['字段名'].lower():
                    print('[warning]字段大小写不同,文件字段:{} 标准字段:{}'.format(
                        field, stand_field['字段名']
                    ))
                else:
                    print('字段不同,文件字段:{} 标准字段:{}'.format(
                        field, stand_field['字段名']
                    ))
                    exit(-1)

        file_info_nums = int(lines[10 + file_field_nums])

        if file_info_nums == 0:
            print('字段数量为0,不往下解析了')
            exit(0)

        file_info_begin_idx = 10 + file_field_nums + 1
        file_infos = lines[file_info_begin_idx: file_info_begin_idx + file_info_nums]

        out_arrays = []

        for info in file_infos:
            current_info = info
            current_dict = {}

            for field_structor in stand_structure:
                length = get_field_len(field_structor['长度'])
                current_dict[field_structor['字段名']] = current_info[:length]
                current_info = current_info[length:]

            out_arrays.append(copy.copy(current_dict))

        for idx, one_info in enumerate(out_arrays):
            out_put_array = []
            for field_structor in stand_structure:
                column_name = field_structor['字段名']
                out_put_array.append('{}:{}'.format(column_name, one_info[column_name]))

            print('[{}] {}'.format(idx + 1, ','.join(out_put_array)))

        columns = []
        for field_structor in stand_structure:
            columns.append(field_structor['字段名'])

        with open('out.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            writer.writerows(out_arrays)
