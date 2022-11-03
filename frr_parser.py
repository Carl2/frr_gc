#!/usr/bin/env python

from frr import parser as fp
from database.sql_db import db_exec, insert_formatter, create_db_file, create_table_fn

test_str = r"""GC      GC-CAP  -M      James Skulczuk  BURRITO - BURRITO - LETOUR      1       430w @4.50wkg   00:42:30.883"""

test_str2 = r"""GC      GC-GHT  -M      Calle Olsen     SZ - SZ LOKE    5       243w @3.80wkg   00:53:00.323"""
DB_FILE = "frr.db"




def main():
    handler = create_db_file(DB_FILE)
    # rider1 = fp.GcRow(test_str)
    # rider2 = fp.GcRow(test_str2)
    # insert_formatter = db.insert_formatter(column_names=fp.GcRow.tabulate_columns(), table_name="Rider")
    # tbl = [rider1.tabulate(), rider2.tabulate()]
    # print(insert_formatter(tbl))
    table_create_fn = create_table_fn(handler.cursor())
    table_create_fn(column_names=fp.GcRow.tabulate_columns(), table_name="riders")
    db_format_fn = insert_formatter(column_names=fp.GcRow.tabulate_columns(), table_name="riders")

    rows = [test_str, test_str2]
    fp.pipe_line_insert_row_db(rows=rows,
                               formatter=db_format_fn,
                               db_insert_fn=db_exec(handler=handler.cursor()))

if __name__ == '__main__':
    main()
