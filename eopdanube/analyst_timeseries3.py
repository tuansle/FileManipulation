# Copyright (c) 2014, Vienna University of Technology (TU Wien), Department of
# Geodesy and Geoinformation (GEO).
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of the FreeBSD Project.


'''
Created On 2015-11-05 Don 14:50:27

General description of this module

@author: Senmao Cao senmao.cao@geo.tuwien.ac.at
'''

import numpy as np
from TSAnalyst.Analyst import Analyst
from TSAnalyst.Parameter import ParameterBoolean
from TSAnalyst.Parameter import ParameterFloat
from TSAnalyst.Parameter import ParameterString
from TSAnalyst.Parameter import ParameterSingleDatasetSelection
# from matplotlib import dates
from TSAnalyst.Parameter import ParameterMultipleDatasetSelection


class TimeSeries3Analyst(Analyst):
    def __init__(self):
        # init paramters
        super(TimeSeries3Analyst, self).__init__()
        self.add_param(ParameterMultipleDatasetSelection("Datasets"))
        self.add_param(ParameterFloat("Scale"))
        self.add_param(ParameterFloat("YAxis Max"))
        self.add_param(ParameterFloat("YAxis Min"))
        self.add_param(ParameterString("Color1"))
        self.add_param(ParameterFloat("Graph Element1"))
        self.add_param(ParameterMultipleDatasetSelection("Datasets2"))
        self.add_param(ParameterFloat("Scale2"))
        self.add_param(ParameterFloat("YAxis Max2"))
        self.add_param(ParameterFloat("YAxis Min2"))
        self.add_param(ParameterString("Color2"))
        self.add_param(ParameterString("Graph Element2"))
        self.add_param(ParameterMultipleDatasetSelection("Datasets3"))
        self.add_param(ParameterFloat("Scale3"))
        self.add_param(ParameterFloat("YAxis Max3"))
        self.add_param(ParameterFloat("YAxis Min3"))
        self.add_param(ParameterString("Color3"))
        self.add_param(ParameterString("Graph Element3"))

        # self.add_param(ParameterBoolean("Day of Year", default=False))
        self.add_param(ParameterFloat("Font Size"))
        self.colors = [(1, 0, 0),
                       (0, 1, 0),
                       (0, 0, 1),
                       (0.784, 0.494, 0.812),
                       (0.122, 0.471, 0.706),
                       (0.671, 0.537, 0),
                       (0.106, 0.757, 0.694),
                       (0.475, 0.067, 0.859),
                       (0.043, 0.314, 0.125),
                       (0.961, 0.918, 0.098)]
        for x in range(256 - len(self.colors)):
            self.colors.append(np.random.rand(3, 1))

    @staticmethod
    def analyst_name():
        return "Time Series 3"

    def plot(self, figure, info, params):
        timeseries = params["Datasets"]
        scale = params["Scale"]
        y_max = params["YAxis Max"]
        y_min = params["YAxis Min"]
        color1 = params["Color1"]
        element1 = params["Graph Element1"]
        font_size = params["Font Size"]
        # disable day of the year function
        is_doy = None

        timeseries2 = params["Datasets2"]
        scale2 = params["Scale2"]
        y_max2 = params["YAxis Max2"]
        y_min2 = params["YAxis Min2"]
        color2 = params["Color2"]
        element2 = params["Graph Element2"]

        timeseries3 = params["Datasets3"]
        scale3 = params["Scale3"]
        y_max3 = params["YAxis Max3"]
        y_min3 = params["YAxis Min3"]
        color3 = params["Color3"]
        element3 = params["Graph Element3"]

        # prepare figure
        ax1 = figure.add_subplot(111)
        figure.subplots_adjust(right=1.55)
        # ax.set_title("Time Series")
        # ax.set_xlabel("Day of Year" if is_doy else "Time")
        ax1.grid(False)
        if y_max:
            ax1.set_ylim(top=y_max)
        if y_min:
            ax1.set_ylim(bottom=y_min)
        # ax.set_ylabel("Datasets")


        ax2 = ax1.twinx()
        ax2.grid(False)

        if y_max2:
            ax2.set_ylim(top=y_max2)
        if y_min2:
            ax2.set_ylim(bottom=y_min2)
        # ax2.set_ylabel("Datasets2")

        ax3 = ax1.twinx()
        ax3.grid(False)

        # move the spine of the second axes outwards
        ax3.spines["right"].set_visible(True)
        ax3.spines["right"].set_position(("axes", 1.1))
        ax3.set_frame_on(True)
        ax3.patch.set_visible(False)

        if y_max3:
            ax3.set_ylim(top=y_max3)
        if y_min3:
            ax3.set_ylim(bottom=y_min3)
        # ax2.set_ylabel("Datasets3")



        # plot time series 1
        dataset1_name = None
        for i, ts in enumerate(timeseries):
            if is_doy:
                ts_data = ts.read(doy=True)
            else:
                ts_data = ts.read()

            info.append("=" * len(ts.dataset.name))
            info.append(ts.dataset.name)
            # check if location is out of extent
            if ts_data is None:
                info.append("Error in reading time series!")
                continue

            # check if no valid data available
            if ts_data[0].size < 1:
                info.append("No valid measurement available!")
                continue

            times, data = ts_data
            if scale:
                data = data * scale

            # print stats
            info.append("Number of Measurement: {:d}".format(len(data)))
            stats_str = "Min={:f}, Max={:f}, Mean={:f}, Stdv={:f}".format(np.min(data),
                                                                          np.max(data),
                                                                          np.mean(data),
                                                                          np.std(data))
            info.append(stats_str)
            p1 = None
            if color1 or element1:
                p1, = ax1.plot(times, data, element1, color=color1, label=ts.dataset.name)
            else:
                p1, = ax1.plot(times, data, "o-", color=self.colors[i + 1 % len(self.colors)], label=ts.dataset.name)

        # plot time series 2
        times2 = None
        data2 = None
        for i, ts in enumerate(timeseries2):
            if is_doy:
                ts_data = ts.read(doy=True)
            else:
                ts_data = ts.read()

            info.append("=" * len(ts.dataset.name))
            info.append(ts.dataset.name)
            # check if location is out of extent
            if ts_data is None:
                info.append("Error in reading time series!")
                continue

            # check if no valid data available
            if ts_data[0].size < 1:
                info.append("No valid measurement available!")
                continue

            times, data = ts_data
            if scale2:
                data = data * scale2

            # put times out for Climatologic Mean ssm
            times2 = times
            data2 = data

            # print stats
            info.append("Number of Measurement: {:d}".format(len(data)))
            stats_str = "Min={:f}, Max={:f}, Mean={:f}, Stdv={:f}".format(np.min(data),
                                                                          np.max(data),
                                                                          np.mean(data),
                                                                          np.std(data))
            info.append(stats_str)
            p2 = None
            if color2 or element2:
                p2, = ax2.plot(times, data, element2, color=color2, label=ts.dataset.name)
            else:
                p2, = ax2.plot(times, data, "o-", color=self.colors[i + 1 % len(self.colors)], label=ts.dataset.name)


                # plot time series 3: Climatologic Mean SSM
        for i, ts in enumerate(timeseries3):
            if is_doy:
                ts_data = ts.read(doy=True)
            else:
                ts_data = ts.read()

            info.append("=" * len(ts.dataset.name))
            info.append(ts.dataset.name)
            # check if location is out of extent
            if ts_data is None:
                info.append("Error in reading time series!")
                continue

            # check if no valid data available
            if ts_data[0].size < 1:
                info.append("No valid measurement available!")
                continue

            times, data = ts_data
            if scale3:
                data = data * scale3

            # copy time ranges of times series2 but use data from Climatologic Mean SSM
            for timesx in times2:
                for timesy in times:
                    if timesx.month == timesy.month:
                        data2[times2.tolist().index(timesx)] = data[times.tolist().index(timesy)]

            # print stats
            info.append("Number of Measurement: {:d}".format(len(data)))
            stats_str = "Min={:f}, Max={:f}, Mean={:f}, Stdv={:f}".format(np.min(data),
                                                                          np.max(data),
                                                                          np.mean(data),
                                                                          np.std(data))
            info.append(stats_str)
            p3 = None
            if color3 or element3:
                p3, = ax3.plot(times2, data2, element3, color=color3, label=ts.dataset.name)
            else:
                p3, = ax3.plot(times2, data2, "o-", color=self.colors[i % len(self.colors)], label=ts.dataset.name)

        # legend
        lines = [p2, p3]
        ax1.legend([p1], [dataset1_name], loc='upper right')
        ax1.grid(linestyle=':', linewidth=0.5)
        ax2.legend(lines, [l.get_label() for l in lines], loc='upper left')

        # ax.yaxis.label.set_color(p1.get_color())
        # ax2.yaxis.label.set_color(p2.get_color())
        # ax3.yaxis.label.set_color(bar.get_color())
        if font_size:
            ax1.tick_params(labelsize=font_size)
            ax2.tick_params(labelsize=font_size)
            ax3.tick_params(labelsize=font_size)
        figure.tight_layout()

        return None
