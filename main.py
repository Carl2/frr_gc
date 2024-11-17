#!/usr/bin/env python
from frr2.gc_data import *
import matplotlib.pyplot as plt
from icecream import ic
import numpy as np

data=[[1, "M-GHT", 11, "Daniel Bash (SZ) (GHT)", "SZ", "23 m 47.266 s", "+45.269 s"], [1, "M-GHT", 25, "Jan Odeskog [SZ](GHT)", "SZ", "23 m 53.423 s", "+51.426 s"], [1, "M-GHT", 62, "Jesper Johansson [SZ](GHT)", "SZ", "24 m 15.887 s", "+1 m 13.890 s"], [1, "M-GHT", 74, "Kenneth Söderberg [SZ]", "SZ", "24 m 20.908 s", "+1 m 18.911 s"], [1, "M-GHT", 94, "Calle Olsen [SZ]", "SZ", "24 m 33.298 s", "+1 m 31.301 s"], [1, "M-GHT", 118, "Mattias Sjöberg [SZ]", "SZ", "24 m 53.217 s", "+1 m 51.220 s"], [1, "M-GHT", 153, "Johan Wetterlöv [SZ]", "SZ", "25 m 34.460 s", "+2 m 32.463 s"], [2, "M-GHT", 9, "Mattias Sjöberg [SZ]", "SZ", "1 hrs, 9 m 53.263 s", "+45.240 s"], [2, "M-GHT", 18, "Jan Odeskog [SZ](GHT)", "SZ", "1 hrs, 11 m 21.125 s", "+54.606 s"], [2, "M-GHT", 33, "Daniel Bash (SZ) (GHT)", "SZ", "1 hrs, 11 m 9.645 s", "+1 m 47.008 s"], [2, "M-GHT", 57, "Calle Olsen [SZ]", "SZ", "1 hrs, 11 m 28.794 s", "+3 m 9.744 s"], [2, "M-GHT", 73, "Jesper Johansson [SZ](GHT)", "SZ", "1 hrs, 12 m 51.927 s", "+3 m 43.904 s"], [2, "M-GHT", 105, "Johan Wetterlöv [SZ]", "SZ", "1 hrs, 15 m 7.821 s", "+5 m 59.798 s"], [2, "M-GHT", 128, "Kenneth Söderberg [SZ]", "SZ", "1 hrs, 17 m 30.033 s", "+8 m 22.010 s"], [3, "M-GHT", 2, "Daniel Bash (SZ) (GHT)", "SZ", "1 hrs, 20 m 45.682 s", "+1.000 s"], [3, "M-GHT", 30, "Jesper Johansson [SZ](GHT)", "SZ", "1 hrs, 22 m 3.993 s", "+1 m 19.311 s"], [3, "M-GHT", 76, "Mattias Sjöberg [SZ]", "SZ", "1 hrs, 20 m 27.649 s", "+3 m 6.916 s"], [3, "M-GHT", 77, "Calle Olsen [SZ]", "SZ", "1 hrs, 20 m 25.828 s", "+3 m 8.267 s"], [3, "M-GHT", 90, "Kenneth Söderberg [SZ]", "SZ", "1 hrs, 21 m 53.964 s", "+4 m 36.403 s"], [3, "M-GHT", 95, "Johan Wetterlöv [SZ]", "SZ", "1 hrs, 23 m 31.155 s", "+4 m 52.811 s"], [4, "M-GHT", 1, "Jesper Johansson [SZ](GHT)", "SZ", "41 m 11.396 s", ""], [4, "M-GHT", 4, "Daniel Bash (SZ) (GHT)", "SZ", "40 m 53.376 s", "+2.075 s"], [4, "M-GHT", 18, "Mattias Sjöberg [SZ] (GHT", "SZ", "41 m 25.711 s", "+14.315 s"], [4, "M-GHT", 39, "Kenneth Söderberg [SZ]", "SZ", "42 m 33.518 s", "+1 m 22.122 s"], [4, "M-GHT", 75, "Calle Olsen [SZ]", "SZ", "44 m 43.382 s", "+2 m 31.026 s"], [5, "M-GHT", 21, "Daniel Bash (SZ) (GHT)", "SZ", "45 m", "+1 m 15.420 s"], [5, "M-GHT", 55, "Jesper Johansson [SZ](GHT)", "SZ", "45 m 53.706 s", "+2 m 8.388 s"], [5, "M-GHT", 56, "Mattias Sjöberg [SZ] (GHT", "SZ", "45 m 56.389 s", "+2 m 11.071 s"], [5, "M-GHT", 64, "Kenneth Söderberg [SZ]", "SZ", "46 m 15.622 s", "+2 m 30.304 s"], [5, "M-GHT", 76, "Calle Olsen [SZ]", "SZ", "46 m 30.242 s", "+2 m 44.924 s"], [6, "M-GHT", 6, "Mattias Sjöberg [SZ] (GHT", "SZ", "52 m 27.125 s", "+1.153 s"], [6, "M-GHT", 20, "Jesper Johansson [SZ](GHT)", "SZ", "52 m 15.399 s", "+26.968 s"], [6, "M-GHT", 32, "Kenneth Söderberg [SZ]", "SZ", "52 m 32.354 s", "+43.923 s"], [6, "M-GHT", 34, "Calle Olsen [SZ]", "SZ", "52 m 33.009 s", "+44.578 s"], [6, "M-GHT", 49, "Daniel Bash (SZ) (GHT)", "SZ", "53 m 24.305 s", "+2 m 3.887 s"], [6, "M-GHT", 50, "Stephan Mißfeldt [ZRG-R]", "ZRG-R", "53 m 33.171 s", "+2 m 12.753 s"], [7, "M-GHT", 1, "Jesper Johansson [SZ](GHT)", "SZ", "47 m 50.544 s", ""], [7, "M-GHT", 5, "Mattias Sjöberg [SZ] (GHT", "SZ", "48 m 44.758 s", "+3.917 s"], [7, "M-GHT", 21, "Daniel Bash (SZ) (GHT)", "SZ", "49 m 2.433 s", "+42.061 s"], [7, "M-GHT", 55, "Kenneth Söderberg [SZ]", "SZ", "49 m 56.709 s", "+2 m 6.165 s"], [7, "M-GHT", 67, "Calle Olsen [SZ]", "SZ", "51 m 42.103 s", "+2 m 49.426 s"], [8, "M-GHT", 19, "Jesper Johansson [SZ](GHT)", "SZ", "44 m 45.551 s", "+1 m 7.125 s"], [8, "M-GHT", 22, "Daniel Bash (SZ) (GHT)", "SZ", "44 m 59.389 s", "+1 m 20.963 s"], [8, "M-GHT", 39, "Mattias Sjöberg [SZ] (GHT", "SZ", "45 m 34.951 s", "+1 m 56.525 s"], [8, "M-GHT", 42, "Kenneth Söderberg [SZ]", "SZ", "45 m 36.822 s", "+1 m 58.396 s"], [8, "M-GHT", 43, "Calle Olsen [SZ]", "SZ", "45 m 39.287 s", "+2 m .861 s"], [9, "M-GHT", 18, "Mattias Sjöberg [SZ] (GHT", "SZ", "1 hrs, 40 m 5.361 s", "+2 m 18.358 s"], [9, "M-GHT", 22, "Jesper Johansson [SZ](GHT)", "SZ", "1 hrs, 40 m 50.637 s", "+3 m 3.634 s"], [9, "M-GHT", 39, "Daniel Bash (SZ) (GHT)", "SZ", "1 hrs, 45 m 37.489 s", "+6 m 48.655 s"], [9, "M-GHT", 52, "Calle Olsen [SZ]", "SZ", "1 hrs, 46 m 18.314 s", "+8 m 31.311 s"], [9, "M-GHT", 75, "Kenneth Söderberg [SZ]", "SZ", "1 hrs, 52 m 30.049 s", "+14 m 43.046 s"], [10, "M-GHT", 1, "Jesper Johansson [SZ](GHT)", "SZ", "1 hrs, 20 m 1.987 s", ""], [10, "M-GHT", 14, "Mattias Sjöberg [SZ] (GHT", "SZ", "1 hrs, 21 m 17.099 s", "+1 m 13.965 s"], [10, "M-GHT", 26, "Kenneth Söderberg [SZ]", "SZ", "1 hrs, 23 m 54.443 s", "+2 m 55.452 s"], [10, "M-GHT", 27, "Calle Olsen [SZ]", "SZ", "1 hrs, 23 m 58.251 s", "+2 m 59.260 s"], [10, "M-GHT", 38, "Daniel Bash (SZ) (GHT)", "SZ", "1 hrs, 23 m 46.896 s", "+3 m 44.909 s"]]
data_hdr=["Stage", "Cat", "Pos", "Name", "Team", "Time", "Egap"]


def plot_rider_times(rider_struct, names, stage_numbers):
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(12, 8))

    # Iterate over each rider
    for name in names:
        times = []
        for stage in stage_numbers:
            arr = rider_struct[name]['stages'][stage]['Time'].to_numpy()
            if len(arr) == 0:
                #arr = np.array(['1900-01-01T00:23:53.423000000'], dtype='datetime64')
                arr = np.array(['nat'], dtype='datetime64')
            ic(arr)
            times.append(arr)

            # else:
            #     ic(times)
            #     times.append(np.datetime64('1970-01-01T00:00:00'))

        # Plot times, convert to numerical values for plotting

        ax.plot(stage_numbers, times, marker='o', label=name)

    # Format times on y-axis
    ax.yaxis_date()

    # Set plot labels and legend
    ax.set_title('Rider Times by Stage')
    ax.set_xlabel('Stage Number')
    ax.set_ylabel('Time')
    plt.legend(title='Riders')

    # Show plot
    plt.show()



def main():
  #This creates a Df , with names as index.
  new_pd = create_data(data=data,header=data_hdr)
  new_pd = convert_pd_time(new_pd)
  #print(new_pd)
  # We now need to extract all names that are unique!
  column_fn=make_column_filter(new_pd)
  names=column_fn('Name').value.unique()
  # and unique stages
  stages=column_fn('Stage').value.unique()
  # for each rider , get the time for a stage.
  name_fn = get_field_fn(new_pd, 'Name')
  stage_fn = get_field_fn(new_pd, 'Stage')
  #print(f"{stage_fn(1)}")


  #plot_data = list(map(get_plot_data(name_fn),names))
  #ic(plot_data)

  #riders =[name_fn(name) for name in names]
  rider_struct = create_rider_struct(new_pd, stages, names)

  ic(rider_struct[names[4]]['stages'][9]['Time'])


  #pprint([ str(time).split('T')[1] for time in riders[4]['Time'].to_numpy()])

  #plot_name(names, plot_data, stages)
  plot_rider_times(rider_struct, names, stages)

if __name__ == '__main__':
    main()
