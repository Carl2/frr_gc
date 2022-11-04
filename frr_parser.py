#!/usr/bin/env python
#import sqlite3
import argparse
from frr import parser as fp
from database.sql_db import db_exec, insert_formatter, create_db_file, create_table_fn

test_str = r"""GC      GC-CAP  -M      James Skulczuk  BURRITO - BURRITO - LETOUR      1       430w @4.50wkg   00:42:30.883"""

test_str2 = r"""GC      GC-GHT  -M      Calle Olsen     SZ - SZ LOKE    5       243w @3.80wkg   00:53:00.323"""
DB_FILE = "frr.db"


def parse_arguments():
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        description='Create a database from frr text')
    parser.add_argument('--file', dest='frr_text_file',
                        help='Frr text file', required=True)
    parser.add_argument('--db',
                        dest='db_file',
                        help='Frr text file')
    return parser.parse_args()



def read_raw_file(file_name):
    """Read raw file from frr.
    Keyword Arguments:
    file_name -- Filename
    """
    with open(file_name) as fh:
        rows = fh.readlines()
    return rows


def main():
    arg_parse = parse_arguments()
    rows = read_raw_file(arg_parse.frr_text_file)
    riders = [fp.GcRow(row) for row in rows]

    handler = create_db_file(DB_FILE)
    #rider1 = fp.GcRow(test_str)
    #rider2 = fp.GcRow(test_str2)
    insert_formatter_fn = insert_formatter(column_names=fp.GcRow.tabulate_columns(), table_name="riders")
    table_create_fn = create_table_fn(handler.cursor())
    #rows = [test_str, test_str2]

    try:
        table_create_fn(column_names=fp.GcRow.tabulate_columns(), table_name="riders")
        fp.pipe_line_insert_row_db(rows=rows,
                                   formatter=insert_formatter_fn,
                                   db_insert_fn=db_exec(handler=handler.cursor()))

        handler.commit()
    except Exception as E:
        print(E)





if __name__ == '__main__':
    main()
