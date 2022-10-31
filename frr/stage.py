#import ipdb
import time
import functools

class TourRider:

    def __init__(self, stage_rider):
        """docstring"""
        self.name = stage_rider.name
        self.stages = [stage_rider]

    def add_stage(self, stage_rider):
        """Keyword Arguments: stage -- new stage to be added, check
        so it doesn't already exists."""

        def match_stages(rider):
            #ipdb.set_trace()
            return rider.stage == stage_rider.stage

        stage_list = filter(match_stages, self.stages)

        if len(list(stage_list)) == 0:
            self.stages.append(stage_rider)
        else:
            print("{} Alread has a stage #{}".format(self.name, stage_rider.stage))


    def __str__(self):
        """String representation."""
        str = "{} ".format(self.name, )
        for stage in self.stages:
            str += "\"{}\"".format(stage)
        return str

    def tab_row(self, rider):
        return [rider.stage, rider.watt, rider.wkg, time.strftime("%H:%M:%S",rider.time)]

    def watt_avg(self):
        sum_watt = 0
        for stage in self.stages:
            sum_watt += stage.watt

        return sum_watt/len(self.stages)


    def tabulate(self):
        """Summary.
        stages = 1,2,3,4
        """
        tab = [self.tab_row(stage) for stage in self.stages]
        tab.append(["Sum","Avg","Avg","Total"])
        tab.append([len(self.stages), "{:.2f}".format(self.watt_avg())])
        tab.append([])
        return tab

    def tabulate_header(self):
        return ["Stage", "Watt", "Wkg", "time"]



def create_tour_rider(rider, dic):
    """"Create a TourRider."""
    if rider.name in dic:
        dic[rider.name].add_stage(rider)
    else:
        dic[rider.name] = TourRider(rider)

    return dic


def add_rider_to_stage(stage_dic,tour_rider,stage):
    """
    Keyword Arguments:
    stage_dic  -- dictionary to use
    tour_rider -- Rider to add
    stage      -- stage name
    """
    if stage in stage_dic:
        stage_dic[stage].append(tour_rider)
    else:
        stage_dic[stage] = [tour_rider]
    return stage_dic


def create_stage_dic(stage_dic, tour_rider):
    """
    Keyword Arguments:
    dic        -- Dictionary to use.
    tour_rider -- TourRider
    """
    [add_rider_to_stage(stage_dic, tour_rider, stage.stage) for stage in tour_rider.stages ]


def create_tour(list_stage_riders):
    """
    Keyword Arguments:
    list_stage_riders -- list of riders

    some of the riders are extracted multiple times
    """

    name_dic = {}
    stage_dic = {}
    [create_tour_rider(rider, name_dic) for rider in list_stage_riders]
    [create_stage_dic(stage_dic, tour_rider) for (name, tour_rider) in name_dic.items() ]
    return (name_dic,stage_dic)



def main():
    import frr_gc
    tbl=[
        ["GC", "GC-GHT", "-M", "Ian Coveny", "CRCAF - FoundationNation", 1, "410w @4.10wkg", "00:45:04.294"],
        ["GC", "GC-GHT", "-M", "Ian Coveny", "CRCAF - FoundationNation", 1, "410w @4.10wkg", "00:45:04.294"],
        ["GC", "GC-GHT", "-M", "Ian Coveny", "CRCAF - FoundationNation", 2, "410w @4.10wkg", "00:45:04.294"],
        ["GC", "GC-GHT", "-M", "Patrick Caisse", "LWATT - MWoFosCC", 1, "314w @4.10wkg", "00:45:14.044"],
        ["GC", "GC-GHT", "-M", "Jason Bridges", "RELENTLESS - RELENTLESS - LETOUR", 1, "336w @4.10wkg", "00:45:15.217"],
        ["GC", "GC-GHT", "-M", "Jason Bridges", "RELENTLESS - RELENTLESS - LETOUR", 2, "336w @4.10wkg", "00:45:15.217"]
    ]

    stage_riders = [frr_gc.table_parser(row, frr_gc.TableType.GC) for row in tbl]
    name_dict, stage_dict = create_tour(stage_riders)


    print(len(stage_dict[2]))



if __name__ == '__main__':
    main()
