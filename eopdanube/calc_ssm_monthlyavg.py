from __future__ import division
import os
from sgrt.common.formats.geotiff.read_tiff import read_tiff
from sgrt.common.formats.geotiff.write_tiff import write_tiff
from osgeo import gdal
import numpy as np
from datetime import datetime
from shutil import copy2

def calc_ssm_anomaly(folder_s1, folder_ascat, combine_s1b):
    # create the monthly average dataset for Sentinel-1 SSM, separate S1A and combine S1A+S1B

    end_time = datetime(2016, 12, 31)
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
                    time = datetime.strptime(f_ascat[1:16], '%Y%m%d_%H%M%S')
                    if time < end_time:
                        ascat_time.append(time)
            # try:
            if f[19:22] == 'SSM' and f[29:32] == 'S1A' and f.endswith("tif"):
                date_ssm = datetime.strptime(f[1:16], '%Y%m%d_%H%M%S')
                if date_ssm < end_time:
                    s1_ssm_proc_list.append(f)
                    # find the corresponding ascat image
                    for f_ascat in ascat_ssm_list:
                        min_dif_scene = min(ascat_time, key=lambda d: abs(d - date_ssm))
                        if f_ascat.startswith('D' + min_dif_scene.strftime('%Y%m%d_%H%M%S')):
                            # make sure they have overlap (>50%)
                            f_arr, f_arr_tags = read_tiff(os.path.join(folder_s1, f))
                            f_ascat_arr, f_ascat_arr_tags = read_tiff(os.path.join(folder_ascat, f_ascat))
                            percent_overlap = calculate_percent_overlap(f_arr, f_ascat_arr)
                            if percent_overlap > 0.5:
                                ascat_ssm_proc_list.append(f_ascat)
                                print f, f_ascat, percent_overlap
                                proc_ssm_time.append(date_ssm)
                                proc_ascat_time.append(min_dif_scene)
                                #move the file
                                copy2(os.path.join(folder_ascat, f_ascat), os.path.join(folder_ascat, '../tuan_closest'))

                            else:
                                try:
                                    ascat_time.remove(min_dif_scene)
                                except Exception as e:
                                    print e
                                continue


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










    #
    # # go through the loop of ssm tif files in list
    # for ssmfile in ssm_list:
    #     try:
    #         if ssmfile[19:28] == "MMENSSM--" and ssmfile[1:5] != '9999':
    #             # read tif file to array
    #             ssm_arr, ssm_arr_tag = read_tiff(os.path.join(folderC01_tile, ssmfile))
    #
    #             # find mean and sdv ssm in B02 folder, if there are two images, raise an error
    #             for fil in os.listdir(folderB02_tile):
    #                 if fil.endswith(".tif"):
    #                     if fil[19:28] == "MSTDSSM--" and fil[1:5] == '9999':
    #                         if fil[5:9] == ssmfile[5:9] and fil[14:18] == ssmfile[14:18]:
    #                             stdssm_arr, stdssm_arr_tag = read_tiff(os.path.join(folderB02_tile, fil))
    #                             stdssm_arr = stdssm_arr.astype(np.float32)
    #
    #                     elif fil[19:28] == "MMENSSM--" and fil[1:5] == '9999':
    #                         if fil[5:9] == ssmfile[5:9] and fil[14:18] == ssmfile[14:18]:
    #                             menssm_arr, menssm_arr_tag = read_tiff(os.path.join(folderB02_tile, fil))
    #                             menssm_arr = menssm_arr.astype(np.float32)
    #
    #             # define mask
    #             # mask
    #             mask = (ssm_arr > 200)
    #
    #             ssm_arr_tag['datatype'] = np.float32
    #             # print ssm_arr_tag
    #             ssm_arr = ssm_arr.astype(np.float32)
    #             # calculate sm anomaly
    #             # print ssm_arr
    #             # print "minmax", np.amin(ssm_arr), np.amax(ssm_arr)
    #             # print "ssm 600", ssm_arr[600,600], "ssmmen 600", menssm_arr[600,600]
    #             image_arr = (ssm_arr - menssm_arr) / stdssm_arr
    #             # print "out 600", image_arr[600,600]
    #             # print "ssm", ssm_arr[600, 600], "men", menssm_arr[600, 600], "result", image_arr[600, 600]
    #             image_arr[mask] = 255
    #             # print np.amin(image_arr), np.amax(image_arr)
    #             # write to file
    #             # ct = gdal.ColorTable()
    #             # ct.SetColorEntry(0, (0, 0, 0, 255))
    #             # ct.SetColorEntry(1, (0, 255, 0, 255))
    #             # ct.SetColorEntry(2, (255, 0, 0, 255))
    #             # ct.SetColorEntry(3, (255, 0, 255, 255))
    #             write_tiff(os.path.join(outfolder_tile, ssmfile.replace("MMENSSM--", "SSMANOM--")),
    #                        src_arr=image_arr,
    #                        tags_dict=ssm_arr_tag)
    #             # pyplot.imsave(os.path.join(outfolder_tile, ssmfile.replace("SSM------", "SSMANOM--")), image_arr)
    #     except Exception, e:
    #         print "error with", ssmfile, e


if __name__ == "__main__":
    calc_ssm_anomaly(
        folder_s1='/home/tle/shares/radar/Datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm/C1003/EQUI7_EU500M/E048N012T6/ssm/',
        folder_ascat='/home/tle/data/DATAPROCESSING/eopdanube/METOP_ASCAT/SMO12R/products/datasets/ssm/C0102/EQUI7_EU500M/E048N012T6/original',
        combine_s1b=False)
