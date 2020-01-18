#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, argparse, csv
from collections import OrderedDict


def count_keyword(filepath, keyword, username, pattern_date=r'(\d+/\d+)/\d+\((月|火|水|木|金)\)$'):

    re_date = re.compile(pattern_date)

    with open(filepath) as f:
     lines = f.readlines()
    
    dict = OrderedDict()
    for i, line in enumerate(lines) :
        if line == '\n' :
            continue
        
        str_list = line.split('\t')
        
        if str_list == []:
            continue
        
        if re_date.match(str_list[0]):
            date = re_date.match(str_list[0]).group(1)
        elif len(str_list) == 3:
            name = str_list[1]
            str = str_list[2]
        else:
            str = str_list[0]

        try:
            if name == username:
                if not date in dict: dict[date] = 0
                dict[date] += str.count(keyword)
        except NameError:
            continue
    
    return dict


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputpath', '-i', type=str)
    parser.add_argument('--keyword', '-k', type=str)
    parser.add_argument('--username', '-u', type=str)
    args = parser.parse_args()

    dict = count_keyword(args.inputpath, args.keyword, args.username)
    
    output = []
    for key, value in zip(dict.keys(), dict.values()):
        output.append([key, value])
        
    csvfile = open(os.path.splitext(os.path.basename(args.inputpath))[0] + '.csv', 'w')
    writer = csv.writer(csvfile, lineterminator='\n')
    writer.writerows(output)
    
    csvfile.close()
    print('complete')

if __name__ == '__main__' :
    main()
