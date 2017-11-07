from __future__ import division
import os
from sgrt.common.formats.geotiff.read_tiff import read_tiff
from sgrt.common.formats.geotiff.write_tiff import write_tiff
from osgeo import gdal
import numpy as np
import datetime
from shutil import copy2

def calc_ssm_anomaly(folder_s1, folder_ascat, combine_s1b):
    # create the monthly average dataset for Sentinel-1 SSM, separate S1A and combine S1A+S1B
    #v2: by Vahid suggestion: take scenes in 3day ranges

    end_time = datetime.datetime(2016, 12, 31)
    # # create outfolder if it doesn't exist
    # if not os.path.exists(folder_ascat):
    #     os.makedirs(folder_ascat)

    # set folder path
    if not os.path.exists(folder_s1):
        raise Warning("Can't find ssm folder")

    # create folder if it doesn't exist
    if not os.path.exists(folder_ascat):
        os.makedirs(folder_ascat)

    # find all tif ssm file in C01 folder, add to  list
    s1_ssm_list = os.listdir(folder_s1)

    # find all tif ascat ssm file in C01 folder, add to  list
    ascat_ssm_list = os.listdir(folder_ascat)

    # initiate list for averaging
    s1_ssm_proc_list = []
    ascat_ssm_proc_list = []

    # in case of combine s1b
    if combine_s1b:
        print "still testing"
    else:
        # find the closest ascat scene, add to list
        proc_ssm_time = []
        proc_ascat_time = []
        for f in s1_ssm_list:
            # create a list of ascat datetime
            ascat_time = []
            for f_ascat in ascat_ssm_list:
                if f_ascat[19:22] == 'SSM' and f_ascat.endswith("tif"):
                    time = datetime.datetime.strptime(f_ascat[1:16], '%Y%m%d_%H%M%S')
                    if time < end_time:
                        ascat_time.append(time)
            # try:
            time_ascat_choosen = []
            if f[19:22] == 'SSM' and f[29:32] == 'S1A' and f.endswith("tif"):
                date_ssm = datetime.datetime.strptime(f[1:16], '%Y%m%d_%H%M%S')
                if date_ssm < end_time:
                    s1_ssm_proc_list.append(f)
                    # find the corresponding ascat image
                    print '=====', date_ssm
                    for time_ascat in ascat_time:
                        if time_ascat < date_ssm + datetime.timedelta(days=1) and time_ascat > date_ssm - datetime.timedelta(days=1):
                            time_ascat_choosen.append(time_ascat)

            for f_ascat in ascat_ssm_list:
                for time in time_ascat_choosen:
                    if f_ascat.startswith('D' + time.strftime('%Y%m%d_%H%M%S')):
                        copy2(os.path.join(folder_ascat, f_ascat), os.path.join(folder_ascat, 'chosen'))



                                # ascat_ssm_proc_list.append(f_ascat)
                                # print f, f_ascat
                                # f_arr, f_arr_tags = read_tiff(os.path.join(folder_s1, f))
                                # f_ascat_arr, f_ascat_arr_tags = read_tiff(os.path.join(folder_ascat, f_ascat))
                                # if calculate_percent_overlap(f_arr, f_ascat_arr) == 0:


                                # except Exception as e:
                                # print e


def calculate_percent_overlap(array1, array2):
    # calcuate the percentage of overlapping

    # number of pixel not nan in array1
    not_nan_arr1 = np.count_nonzero(~np.isnan(array1)) - (array1 == 255).sum()
    # number of pixel not nan in array2
    not_nan_arr2 = np.count_nonzero(~np.isnan(array2)) - (array2 == 255).sum()

    # turn 0 to 9999, turbn 255 to 0
    array1[array1 == 0] = 9999
    array1[array1 == 255] = 0
    array2[array2 == 0] = 9999
    array2[array2 == 255] = 0

    # number of pixels not nan in the intersection
    not_nan_intersec = np.count_nonzero(np.multiply(array1, array2))

    # return the
    # print not_nan_arr1, not_nan_arr2, not_nan_intersec
    return float(not_nan_intersec / min(not_nan_arr1, not_nan_arr2))




if __name__ == "__main__":
    calc_ssm_anomaly(
        folder_s1='/home/tle/shares/radar/Datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm/C1003/EQUI7_EU500M/E048N012T6/ssm/',
        folder_ascat='/home/tle/data/DATAPROCESSING/eopdanube/METOP_ASCAT/SMO12R/products/datasets/ssm/C0102/EQUI7_EU500M/E048N012T6/',
        combine_s1b=False)
