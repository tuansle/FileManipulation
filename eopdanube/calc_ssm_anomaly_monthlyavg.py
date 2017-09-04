from __future__ import division
import os
from sgrt.common.formats.geotiff.read_tiff import read_tiff
from sgrt.common.formats.geotiff.write_tiff import write_tiff
from osgeo import gdal
import numpy as np


def calc_ssm_anomaly(tile_list, folderB02, folderC01, outfolder):
    # create outfolder if it doesn't exist
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    for til in tile_list:
        # set folder path
        folderB02_tile = os.path.join(folderB02, til)
        folderC01_tile = os.path.join(folderC01, til)
        if not os.path.exists(folderB02) or not os.path.exists(folderC01):
            raise Warning("Can't find parameter or ssm folder")
        outfolder_tile = os.path.join(outfolder, til)

        # create folder if it doesn't exist
        if not os.path.exists(outfolder_tile):
            os.makedirs(outfolder_tile)

        # find all tif ssm file in C01 folder, add to  list
        ssm_list = os.listdir(folderC01_tile)

        # go through the loop of ssm tif files in list
        for ssmfile in ssm_list:
            try:
                if ssmfile[19:28] == "MMENSSM--" and ssmfile[1:5] != '9999':
                    # read tif file to array
                    ssm_arr, ssm_arr_tag = read_tiff(os.path.join(folderC01_tile, ssmfile))

                    # find mean and sdv ssm in B02 folder, if there are two images, raise an error
                    for fil in os.listdir(folderB02_tile):
                        if fil.endswith(".tif"):
                            if fil[19:28] == "MSTDSSM--" and fil[1:5] == '9999':
                                if fil[5:9] == ssmfile[5:9] and fil[14:18] == ssmfile[14:18]:
                                    stdssm_arr, stdssm_arr_tag = read_tiff(os.path.join(folderB02_tile, fil))
                                    stdssm_arr = stdssm_arr.astype(np.float32)

                            elif fil[19:28] == "MMENSSM--" and fil[1:5] == '9999':
                                if fil[5:9] == ssmfile[5:9] and fil[14:18] == ssmfile[14:18]:
                                    menssm_arr, menssm_arr_tag = read_tiff(os.path.join(folderB02_tile, fil))
                                    menssm_arr = menssm_arr.astype(np.float32)

                    # define mask
                    # mask
                    mask = (ssm_arr > 200)

                    ssm_arr_tag['datatype'] = np.float32
                    # print ssm_arr_tag
                    ssm_arr = ssm_arr.astype(np.float32)
                    # calculate sm anomaly
                    # print ssm_arr
                    # print "minmax", np.amin(ssm_arr), np.amax(ssm_arr)
                    # print "ssm 600", ssm_arr[600,600], "ssmmen 600", menssm_arr[600,600]
                    image_arr = (ssm_arr - menssm_arr) / stdssm_arr
                    # print "out 600", image_arr[600,600]
                    # print "ssm", ssm_arr[600, 600], "men", menssm_arr[600, 600], "result", image_arr[600, 600]
                    image_arr[mask] = 255
                    # print np.amin(image_arr), np.amax(image_arr)
                    # write to file
                    # ct = gdal.ColorTable()
                    # ct.SetColorEntry(0, (0, 0, 0, 255))
                    # ct.SetColorEntry(1, (0, 255, 0, 255))
                    # ct.SetColorEntry(2, (255, 0, 0, 255))
                    # ct.SetColorEntry(3, (255, 0, 255, 255))
                    write_tiff(os.path.join(outfolder_tile, ssmfile.replace("MMENSSM--", "SSMANOM--")),
                               src_arr=image_arr,
                               tags_dict=ssm_arr_tag)
                    # pyplot.imsave(os.path.join(outfolder_tile, ssmfile.replace("SSM------", "SSMANOM--")), image_arr)
            except Exception, e:
                print "error with", ssmfile, e
        print "SSM Anomaly processed for ", til


if __name__ == "__main__":
    tile_list = ["E042N018T6",
                 "E042N012T6",
                 "E048N006T6",
                 "E048N012T6",
                 "E048N018T6",
                 "E048N024T6",
                 "E054N006T6",
                 "E054N012T6",
                 "E054N018T6",
                 "E060N006T6",
                 "E060N012T6",
                 "E060N018T6"],

    tile_list_test=["E048N012T6"]

    # #tests1
    # calc_ssm_anomaly(tile_list=tile_list_test,
    #                  folderB02="/home/tle/data/DATAPROCESSING/eopdanube_testmixssm/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU500M",
    #                  folderC01="/home/tle/data/DATAPROCESSING/eopdanube_testmixssm/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU500M",
    #                  outfolder="/data/DATAPROCESSING/eopdanube_testmixssm/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm_anomaly/EQUI7_500M")

    #ASA
    calc_ssm_anomaly(tile_list=tile_list_test,
                     folderB02="/data/DATAPROCESSING/eopdanube_testmixssm/Envisat_ASAR/WS/parameters/datasets/par_stat/B0201/EQUI7_EU500M/",
                     folderC01="/data/DATAPROCESSING/eopdanube_testmixssm/Envisat_ASAR/WS/parameters/datasets/par_stat/B0201/EQUI7_EU500M/",
                     outfolder="/data/DATAPROCESSING/eopdanube_testmixssm/Envisat_ASAR/WS/products/datasets/ssm_anomaly/EQUI7_500M")

    # #
    # calc_ssm_anomaly(tile_list=["E042N018T6",
    #                             "E042N012T6",
    #                             "E048N006T6",
    #                             "E048N012T6",
    #                             "E048N018T6",
    #                             "E048N024T6",
    #                             "E054N006T6",
    #                             "E054N012T6",
    #                             "E054N018T6",
    #                             "E060N006T6",
    #                             "E060N012T6",
    #                             "E060N018T6"],
    #                  folderB02="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Envisat_ASAR/GM/parameters/datasets/par_stat/B0201/EQUI7_EU500M/",
    #                  folderC01="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Envisat_ASAR/GM/parameters/datasets/par_stat/B0201/EQUI7_EU500M/",
    #                  outfolder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Envisat_ASAR/GM/products/datasets/ssm_anomaly/EQUI7_EU500M_Final")
    # #

    #
    # calc_ssm_anomaly(tile_list=["E042N018T6",
    #                             "E042N012T6",
    #                             "E048N006T6",
    #                             "E048N012T6",
    #                             "E048N018T6",
    #                             "E048N024T6",
    #                             "E054N006T6",
    #                             "E054N012T6",
    #                             "E054N018T6",
    #                             "E060N006T6",
    #                             "E060N012T6",
    #                             "E060N018T6"],
    #                  folderB02="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Envisat_ASAR/WS/parameters/datasets/par_stat/B0201/EQUI7_EU500M/",
    #                  folderC01="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Envisat_ASAR/WS/parameters/datasets/par_stat/B0201/EQUI7_EU500M/",
    #                  outfolder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Envisat_ASAR/WS/products/datasets/ssm_anomaly/EQUI7_EU500M_Final")
    #

    #
    # calc_ssm_anomaly(tile_list=["E042N018T6",
    #                             "E042N012T6",
    #                             "E048N006T6",
    #                             "E048N012T6",
    #                             "E048N018T6",
    #                             "E048N024T6",
    #                             "E054N006T6",
    #                             "E054N012T6",
    #                             "E054N018T6",
    #                             "E060N006T6",
    #                             "E060N012T6",
    #                             "E060N018T6"],
    #                  folderB02="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU500M/",
    #                  folderC01="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU500M/",
    #                  outfolder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm_anomaly/EQUI7_EU500M_Final")



    # REDO FIX BUG
    # GM
    # calc_ssm_anomaly(tile_list=["E054N012T6",
    #                             "E060N012T6",
    #                             "E060N018T6"],
    #                  folderB02="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Envisat_ASAR/GM/parameters/datasets/par_stat/B0201/EQUI7_EU500M/",
    #                  folderC01="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Envisat_ASAR/GM/parameters/datasets/par_stat/B0201/EQUI7_EU500M/",
    #                  outfolder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Envisat_ASAR/GM/products/datasets/ssm_anomaly/EQUI7_EU500M_Final")



    # #WS
    # calc_ssm_anomaly(tile_list=["E048N024T6",
    #                             "E054N012T6",
    #                             "E054N018T6",
    #                             "E060N018T6"],
    #                  folderB02="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Envisat_ASAR/WS/parameters/datasets/par_stat/B0201/EQUI7_EU500M/",
    #                  folderC01="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Envisat_ASAR/WS/parameters/datasets/par_stat/B0201/EQUI7_EU500M/",
    #                  outfolder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Envisat_ASAR/WS/products/datasets/ssm_anomaly/EQUI7_EU500M_Final")
