import pandas as pd
import functools
from pymonad.maybe import Just, Nothing, Maybe
from pprint import pprint
from icecream import ic
import numpy as np
from datetime import timedelta


def create_data(*, header: list[str], data: list[list]) -> pd.DataFrame:
    """Create a DataFrame from header and data where the index is the fourth column."""
    return pd.DataFrame(
        data=data,
        columns=header,
        index=[row[3] for row in data]
    )


def get_field_fn(data:pd.DataFrame, field:str ) -> callable:
    def get_df_field(compare):
        df_named = data.loc[data[field] == compare]
        return df_named
    return get_df_field

def get_data_fn(data:pd.DataFrame):

    def fun(field):
        data.loc['Egap']






def make_column_filter(data: pd.DataFrame):
    def column_fn(column: str) -> Maybe:
        try:
            return Just(data[column])
        except Exception:
            return Nothing
    return column_fn


def parse_time(time_str):
    if 'hrs' not in time_str:
        #If hrs is missing, we'll add it.
        time_str = "0 hrs, " + time_str
    if time_str[-1] != 's':
        time_str = time_str + " 0.0 s"
    return pd.to_datetime(time_str, format='%H hrs, %M m %S.%f s')

def parse_delta(delta_str:str):
    """Convert to delta time

    +2 m 12.753 s -> 2*60 + 12.753
    - split
    """
    minutes = 0
    seconds = 0
    if 'm' in delta_str:
        minute_str, sec_str = delta_str.split('m')
        minutes_str = minute_str.strip()[1:]
        minutes = int(minutes_str) * 60
        ic(minutes, delta_str)
        delta_str = '+' + sec_str.strip()


    else:
        delta_str = delta_str

    if 's' in delta_str:
        #second_str = delta_str[1:-2]
        second_str = delta_str[1:-2]
        seconds =float(second_str)

    td = timedelta(seconds=seconds,minutes=minutes)
    ic(delta_str,td)
    # #return minutes+seconds
    return td

def convert_pd_time(df: pd.DataFrame):
    new_df = df.copy()
    new_df['Time'] = new_df['Time'].transform(parse_time)
    new_df['Egap'] = new_df['Egap'].transform(parse_delta)
    return new_df

#Get stage for name.
# f( stages, names)




def get_plot_data(name_fn):

    def plot_data(name):

        val = name_fn(name)
        ic(val.loc[val['Stage'] == 1, 'Time'])
        #ic(val.loc['Stage' == 1 and 'Time'])
        return {name: val['Time'].to_numpy()}

    return plot_data




def create_stage_data(data_field, stages, field):
    """Create stage data fields

    The output from this function should become a dictionary

        {
         1: data_field,
         2: data_field,
         3: data_field
         }

    """
    stage_dic = {}
    stage_fn = get_field_fn(data_field, field)
    for stage in stages:
        val = stage_fn(stage)

        stage_dic[stage] = val
    return stage_dic




def create_rider_struct(df, stages, names):
    """Create data to be able to plot.

    Here is how the data should look

    {<name1> :
      stages: {
              1: data_field,
              2: data_field,
              3: data_field
              }
      egap: {
              1: data_field,
              2: data_field,
              3: data_field
     }],
     <name2> : [
        {1: data_field},
        {3: data_field}
        ....
    }]
    """
    myDic = {}
    name_fn = get_field_fn(df, 'Name')

    for name in names:
        name_df = name_fn(name)
        myDic[name] = {'stages': create_stage_data(name_df, stages, 'Stage')}

    return myDic


def create_array_from_struct(rider_struct: dict, name: str,
                             stages: list[int], field: str,
                             error_fn: callable) -> dict:
    times = []
    for stage in stages:
        arr = rider_struct[name]['stages'][stage][field].to_numpy()
        if len(arr) == 0:
            arr = error_fn()
        times.append(arr[0])
    return times
# egap = rider_struct[name]['stages'][stage]['Egap'].to_numpy()
# ic(egap)
