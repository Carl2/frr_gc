#!/usr/bin/env python
import argparse
from frr import parser as fp
from database.sql_db import db_exec, insert_formatter, open_db_file, create_table_fn
from tabulate import tabulate

DEFAULT_DB_FILE = "frr.db"


def parse_arguments():
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        description='Create a database from frr text')
    parser.add_argument('--file', dest='frr_text_file',
                        help='Frr Raw text file', required=True)
    parser.add_argument('--db',
                        dest='db_file',
                        help='Sqlite database file(output)',
                        default=DEFAULT_DB_FILE
                        )
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
    handler = open_db_file(arg_parse.db_file)
    insert_formatter_fn = insert_formatter(column_names=fp.GcRow.tabulate_columns(),
                                           table_name="riders")
    table_create_fn = create_table_fn(handler.cursor())


    try:
        table_create_fn(column_names=fp.GcRow.tabulate_columns(),
                        table_name="riders")
        stop = 0
        # It seems as if there is a limitation on how many values that
        # can be used, spliting it up in chunks.
        vals = []

        for start in range(0, len(rows),200):
            stop = start +200-1
            vals.append([start,stop])
            fp.pipe_line_insert_row_db(rows=rows[start:stop],
                                       formatter=insert_formatter_fn,
                                       db_insert_fn=db_exec(handler=handler.cursor()))




        handler.commit()
        print(tabulate(vals, headers=["Start","Stop"], tablefmt='orgtbl'))
    except Exception as E:
        print(E)





if __name__ == '__main__':
    main()
