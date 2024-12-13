#!/usr/bin/env python
from functools import reduce
from itertools import takewhile
from icecream import ic
import numpy as np
from datetime import timedelta
from frr2.gc_data import *
import matplotlib.pyplot as plt
from pandas.core.groupby.generic import DataFrameGroupBy
from datetime import datetime,timedelta
from col_iter import split_by

data=[[1, "M-GHT", 11, "Daniel Bash (SZ) (GHT)", "SZ", "23 m 47.266 s", "+45.269 s"], [1, "M-GHT", 25, "Jan Odeskog [SZ](GHT)", "SZ", "23 m 53.423 s", "+51.426 s"], [1, "M-GHT", 62, "Jesper Johansson [SZ](GHT)", "SZ", "24 m 15.887 s", "+1 m 13.890 s"], [1, "M-GHT", 74, "Kenneth Söderberg [SZ]", "SZ", "24 m 20.908 s", "+1 m 18.911 s"], [1, "M-GHT", 94, "Calle Olsen [SZ]", "SZ", "24 m 33.298 s", "+1 m 31.301 s"], [1, "M-GHT", 118, "Mattias Sjöberg [SZ]", "SZ", "24 m 53.217 s", "+1 m 51.220 s"], [1, "M-GHT", 153, "Johan Wetterlöv [SZ]", "SZ", "25 m 34.460 s", "+2 m 32.463 s"], [2, "M-GHT", 9, "Mattias Sjöberg [SZ]", "SZ", "1 hrs, 9 m 53.263 s", "+45.240 s"], [2, "M-GHT", 18, "Jan Odeskog [SZ](GHT)", "SZ", "1 hrs, 11 m 21.125 s", "+54.606 s"], [2, "M-GHT", 33, "Daniel Bash (SZ) (GHT)", "SZ", "1 hrs, 11 m 9.645 s", "+1 m 47.008 s"], [2, "M-GHT", 57, "Calle Olsen [SZ]", "SZ", "1 hrs, 11 m 28.794 s", "+3 m 9.744 s"], [2, "M-GHT", 73, "Jesper Johansson [SZ](GHT)", "SZ", "1 hrs, 12 m 51.927 s", "+3 m 43.904 s"], [2, "M-GHT", 105, "Johan Wetterlöv [SZ]", "SZ", "1 hrs, 15 m 7.821 s", "+5 m 59.798 s"], [2, "M-GHT", 128, "Kenneth Söderberg [SZ]", "SZ", "1 hrs, 17 m 30.033 s", "+8 m 22.010 s"], [3, "M-GHT", 2, "Daniel Bash (SZ) (GHT)", "SZ", "1 hrs, 20 m 45.682 s", "+1.000 s"], [3, "M-GHT", 30, "Jesper Johansson [SZ](GHT)", "SZ", "1 hrs, 22 m 3.993 s", "+1 m 19.311 s"], [3, "M-GHT", 76, "Mattias Sjöberg [SZ]", "SZ", "1 hrs, 20 m 27.649 s", "+3 m 6.916 s"], [3, "M-GHT", 77, "Calle Olsen [SZ]", "SZ", "1 hrs, 20 m 25.828 s", "+3 m 8.267 s"], [3, "M-GHT", 90, "Kenneth Söderberg [SZ]", "SZ", "1 hrs, 21 m 53.964 s", "+4 m 36.403 s"], [3, "M-GHT", 95, "Johan Wetterlöv [SZ]", "SZ", "1 hrs, 23 m 31.155 s", "+4 m 52.811 s"], [4, "M-GHT", 1, "Jesper Johansson [SZ](GHT)", "SZ", "41 m 11.396 s", ""], [4, "M-GHT", 4, "Daniel Bash (SZ) (GHT)", "SZ", "40 m 53.376 s", "+2.075 s"], [4, "M-GHT", 18, "Mattias Sjöberg [SZ] (GHT", "SZ", "41 m 25.711 s", "+14.315 s"], [4, "M-GHT", 39, "Kenneth Söderberg [SZ]", "SZ", "42 m 33.518 s", "+1 m 22.122 s"], [4, "M-GHT", 75, "Calle Olsen [SZ]", "SZ", "44 m 43.382 s", "+2 m 31.026 s"], [5, "M-GHT", 21, "Daniel Bash (SZ) (GHT)", "SZ", "45 m", "+1 m 15.420 s"], [5, "M-GHT", 55, "Jesper Johansson [SZ](GHT)", "SZ", "45 m 53.706 s", "+2 m 8.388 s"], [5, "M-GHT", 56, "Mattias Sjöberg [SZ] (GHT", "SZ", "45 m 56.389 s", "+2 m 11.071 s"], [5, "M-GHT", 64, "Kenneth Söderberg [SZ]", "SZ", "46 m 15.622 s", "+2 m 30.304 s"], [5, "M-GHT", 76, "Calle Olsen [SZ]", "SZ", "46 m 30.242 s", "+2 m 44.924 s"], [6, "M-GHT", 6, "Mattias Sjöberg [SZ] (GHT", "SZ", "52 m 27.125 s", "+1.153 s"], [6, "M-GHT", 20, "Jesper Johansson [SZ](GHT)", "SZ", "52 m 15.399 s", "+26.968 s"], [6, "M-GHT", 32, "Kenneth Söderberg [SZ]", "SZ", "52 m 32.354 s", "+43.923 s"], [6, "M-GHT", 34, "Calle Olsen [SZ]", "SZ", "52 m 33.009 s", "+44.578 s"], [6, "M-GHT", 49, "Daniel Bash (SZ) (GHT)", "SZ", "53 m 24.305 s", "+2 m 3.887 s"], [6, "M-GHT", 50, "Stephan Mißfeldt [ZRG-R]", "ZRG-R", "53 m 33.171 s", "+2 m 12.753 s"], [7, "M-GHT", 1, "Jesper Johansson [SZ](GHT)", "SZ", "47 m 50.544 s", ""], [7, "M-GHT", 5, "Mattias Sjöberg [SZ] (GHT", "SZ", "48 m 44.758 s", "+3.917 s"], [7, "M-GHT", 21, "Daniel Bash (SZ) (GHT)", "SZ", "49 m 2.433 s", "+42.061 s"], [7, "M-GHT", 55, "Kenneth Söderberg [SZ]", "SZ", "49 m 56.709 s", "+2 m 6.165 s"], [7, "M-GHT", 67, "Calle Olsen [SZ]", "SZ", "51 m 42.103 s", "+2 m 49.426 s"], [8, "M-GHT", 19, "Jesper Johansson [SZ](GHT)", "SZ", "44 m 45.551 s", "+1 m 7.125 s"], [8, "M-GHT", 22, "Daniel Bash (SZ) (GHT)", "SZ", "44 m 59.389 s", "+1 m 20.963 s"], [8, "M-GHT", 39, "Mattias Sjöberg [SZ] (GHT", "SZ", "45 m 34.951 s", "+1 m 56.525 s"], [8, "M-GHT", 42, "Kenneth Söderberg [SZ]", "SZ", "45 m 36.822 s", "+1 m 58.396 s"], [8, "M-GHT", 43, "Calle Olsen [SZ]", "SZ", "45 m 39.287 s", "+2 m .861 s"], [9, "M-GHT", 18, "Mattias Sjöberg [SZ] (GHT", "SZ", "1 hrs, 40 m 5.361 s", "+2 m 18.358 s"], [9, "M-GHT", 22, "Jesper Johansson [SZ](GHT)", "SZ", "1 hrs, 40 m 50.637 s", "+3 m 3.634 s"], [9, "M-GHT", 39, "Daniel Bash (SZ) (GHT)", "SZ", "1 hrs, 45 m 37.489 s", "+6 m 48.655 s"], [9, "M-GHT", 52, "Calle Olsen [SZ]", "SZ", "1 hrs, 46 m 18.314 s", "+8 m 31.311 s"], [9, "M-GHT", 75, "Kenneth Söderberg [SZ]", "SZ", "1 hrs, 52 m 30.049 s", "+14 m 43.046 s"], [10, "M-GHT", 1, "Jesper Johansson [SZ](GHT)", "SZ", "1 hrs, 20 m 1.987 s", ""], [10, "M-GHT", 14, "Mattias Sjöberg [SZ] (GHT", "SZ", "1 hrs, 21 m 17.099 s", "+1 m 13.965 s"], [10, "M-GHT", 26, "Kenneth Söderberg [SZ]", "SZ", "1 hrs, 23 m 54.443 s", "+2 m 55.452 s"], [10, "M-GHT", 27, "Calle Olsen [SZ]", "SZ", "1 hrs, 23 m 58.251 s", "+2 m 59.260 s"], [10, "M-GHT", 38, "Daniel Bash (SZ) (GHT)", "SZ", "1 hrs, 23 m 46.896 s", "+3 m 44.909 s"]]
data_hdr=["Stage", "Cat", "Pos", "Name", "Team", "Time", "Egap"]


#Need to convert this time value
# "1 hrs, 23 m 46.896 s" to time delta

def make_time_delta(hours_str: str, minute_str: str,
                    second_str: str, milli_str: str) -> timedelta:
    hours = 0
    minutes = 0
    seconds = 0
    milli = 0
    if hours_str is not None:
        hours = int(hours_str)
    if minute_str is not None:
        minutes = int(minute_str)
    if second_str is not None:
        seconds = int(second_str)
    if milli_str is not None:
        milli = int(milli_str)
    ic(hours, minutes, seconds, milli)
    return timedelta(hours=hours, minutes=minutes,
                     seconds=seconds, milliseconds=milli)

def parse_time_str(time_str):
    time_split = split_by(time_str, ["hrs,", "m", ".", "s"])
    hours = 0
    minutes = 0
    seconds = 0
    milli = 0
    if time_split[0] is not None:
        hours = int(time_split[0])
    if time_split[1] is not None:
        minutes = int(time_split[1])
    if time_split[2] is not None:
        seconds = int(time_split[2])

    if time_split[3] is not None:
        milli = int(time_split[3])

    return timedelta(hours=hours, minutes=minutes,
                     seconds=seconds, milliseconds=milli)

def parse_egap(egap_str:str) -> timedelta:
    #"+2 m 59.260 s"
    parts = split_by(egap_str, ["+","m",".","s"])
    ic(parts)
    td = make_time_delta(None, parts[1], parts[2], parts[3])
    ic(td)
    return td






def convert_to_time_repr(seconds: float):
    return str(timedelta(seconds=seconds))

def handle_stage_name(init_values, stage):
    data = init_values['data']
    vals = init_values['times']
    stage_value = data[data['Stage'] == stage]['Time']

    if len(stage_value) != 0:
        val=stage_value.dt.total_seconds().iloc[0]
        vals[int(stage)-1] = val
    return init_values


def handle_rider(init_values:dict , name_group: DataFrameGroupBy  ):
    name,data = name_group
    unique_stages = init_values['stages']
    ax = init_values['ax']
    times = np.full(len(unique_stages), np.nan)
    rider_vals = reduce(handle_stage_name,unique_stages, {'data': data, 'times': times} )
    ax.plot(unique_stages, rider_vals['times'],'o-', label=name[0])
    ax.set_xticks(unique_stages)
    ax.set_xlabel('Stages')
    init_values[name[0]] = rider_vals['times']
    return init_values




def make_stage_plot(df_orig: pd.DataFrame):
    fig,ax = plt.subplots( figsize=(16,8))
    df = df_orig.copy()

    # Getting the unique stages (1,2,3,4,5....)
    unique_stages = df['Stage'].unique()
    # First we need to create y_values, which means the times for each rider
    name_group = df.groupby(['Name'])
    y_values = reduce(handle_rider, name_group, {'stages': unique_stages, 'ax': ax})
    ax.legend()
    yticks = ax.get_yticks()
    ax.set_yticks(yticks)  # Set the tick positions first
    tm_arr = map(convert_to_time_repr, yticks)
    ax.set_yticklabels(tm_arr, ha='right' )
    output_file = 'plot_rider_times.png'
    plt.savefig(output_file)
    plt.close()

def make_egap_plot(df: pd.DataFrame):
    fix, ax = plt.subplot(figsize=(16, 8))






def main():
    #Lets start by creating a dataframe.

    df = create_data(header=data_hdr, data=data)
    # Fix the times
    df['Time'] = df['Time'].apply(parse_time_str)
    df['Egap'] = df['Egap'].apply(parse_egap)
    ic(df['Egap'])
    make_stage_plot(df)




if __name__ == '__main__':

    main()
