from jinja2 import Template
import sqlite3
import logging

log = logging.getLogger("frr/sql_db")
log.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class SqlDb:
    DB_INSERT_FMT = r"""INSERT INTO {{table}} ({% for item in columns -%}
      {{item}} {{", " if not loop.last else ""}}
    {%- endfor %}) VALUES {{values}};
    """


    DB_VALUE_FIELD = r"""
{%for val in values -%}{{val}} {{ ", " if not loop.last else "" }} {%- endfor %}"""
    # DB_VALUE_FIELD = r"""
    # {% for row in values -%}
    #      ({% for field in row -%}
    #        {{field}} {{ ", " if not loop.last else "" }}
    #      {%- endfor %})
    # {{ ", " if not loop.last else "" }}
    # {%- endfor %}
    # """

    insert_tmpl = Template(DB_INSERT_FMT)
    insert_value_tmpl = Template(DB_VALUE_FIELD)

###############################################################################
#                            Database functionality                           #
###############################################################################
def create_db_file(new_db_file):
    """
    Keyword Arguments:
    new_db_file -- sqlite database file
    """
    con = sqlite3.connect(new_db_file)
    return con

def create_table_fn(db_handler):
    """Retrun function to create a table.
    Keyword Arguments:
    db_conn -- db connection
    """
    def create_table(*,column_names, table_name,):
        column_str = ",".join(column_names)
        str_create = f"CREATE TABLE {table_name}({column_str})"
        log.debug("Create Table str: \"" +str_create + "\"")
        try:
            db_handler.execute(str_create)
        except Exception as E:
            log.critical(f"could not create table {E}")

    return create_table




def db_exec(*, handler):
    """Return a function that can be used to insert into table
    Keyword Arguments:
    handler -- Database handler
    """
    def exec_db(insert_str):
        log.debug(f"About to insert \"{insert_str}\"")
        try:
            handler.execute(insert_str)
        except Exception as e:
            log.critical(f"DB Execute {e} failed with line\n\"{insert_str}\"")

    return exec_db




def insert_formatter(*,column_names, table_name):
    """Create a formatted string for insertion into db.

    Keyword Arguments:
    column_names -- List of column names
    table_name -- table name
    """
    table_columns = ",".join(column_names)
    header=f"INSERT INTO {table_name} VALUES"
    log.debug(f"\"{header}\"")
    # TODO: consider using ','.joint(obj_list)
    def db_insert_values(objs_list):
        """A list of list of things to be added.
        [["a","b"],["c","d"]]
        """

        row_list = [",".join(map(str,row)) for row in objs_list]
        value_list = [f"({obj})" for obj in row_list]

        command = header + ",".join(value_list) + ";"
        log.debug(f"Gen: {command}")
        return command
    return db_insert_values
