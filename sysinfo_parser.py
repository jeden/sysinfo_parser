#!/usr/bin/env python

'''
sysinfo_parser

USAGE: sysinfo_parser file_name [section]
'''

import re, sys

if len(sys.argv) < 2:
        sys.exit(__doc__)

file_name = sys.argv[1]
section_to_print = len(sys.argv) >= 3 and ('[' + sys.argv[2] + ']') or None

f = open(file_name, 'r')
info = f.read()
f.close()

rx_section = re.compile(r'^((\[\w*\])*\r?\n\r?\n)((([\w ]*)\t?)+)(((\r?\n)*(([\w\d \(\)\\/\-:!\?\.,\{\}]*)\t?)+)*)', re.MULTILINE)
rx_header = re.compile(r'([\w ]*)\t?')
rx_data = re.compile(r'^((([\w\d \(\)\\/\-:!\?\.,\{\}]*)\t?)+)', re.MULTILINE)
rx_data_row = re.compile(r'([\w\d \(\)\\/\-:!\?\.,\{\}\[\]]*)\t?')

map = {}

for match_section in rx_section.finditer(info):
        groups = match_section.groups()
        section = groups[1]
        headers = groups[2]
        rows = groups[5]
        #print section

        map[section] = []

        headers = [match_header.groups()[0] for match_header in rx_header.finditer(headers) if len(match_header.groups()[0]) > 0 ]

        if len(headers) > 0 and len(rows) > 0:
                #print headers

                for match_data in rx_data.finditer(rows):
                        groups = match_data.groups()
                        data = groups[0]
                        data_row = [match_data_row.groups()[0] for match_data_row in rx_data_row.finditer(data) if len(match_data_row.groups()[0]) > 0 ]
                        if data_row and len(data_row) >= len(headers):
                                #print data_row
                                row = { key: data_row[index] for index, key in enumerate(headers) }
                                map[section].append(row)

        #print '-' * 100

if section_to_print:
        if map.has_key(section_to_print):
                try:
                        print ','.join(map[section_to_print][0].keys())
                        for row in map[section_to_print]:
                                print ','.join(row.values())
                except:
                        print 'An error occurred while exporting data - most likely a format error'
        else:
                print 'ERROR: Section not found'
else:
        print map

