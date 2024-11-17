import pandas as pd
import functools
from pymonad.maybe import Just, Nothing, Maybe
from pprint import pprint
from icecream import ic


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


def convert_pd_time(df: pd.DataFrame):
    new_df = df.copy()
    new_df['Time'] = new_df['Time'].transform(parse_time)
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




def create_stage_data(data_field, stages):
    """Create stage data fields

    The output from this function should become a dictionary

        {
         1: data_field,
         2: data_field,
         3: data_field
         }

    """
    stage_dic = {}
    stage_fn = get_field_fn(data_field, 'Stage')
    for stage in stages:
         stage_dic[stage] = stage_fn(stage)
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
     <name2> :
        {1: data_field},
        {3: data_field}
        ....
    }
    """
    myDic = {}
    name_fn = get_field_fn(df, 'Name')
    for name in names:
        name_df = name_fn(name)
        stage_dic = {}
        stage_dic['stages'] = create_stage_data(name_df, stages)
        myDic[name] = stage_dic
    return myDic
