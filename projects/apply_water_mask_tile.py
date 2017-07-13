import os
from sgrt.common.formats.geotiff.read_tiff import read_tiff
from sgrt.common.formats.geotiff.write_tiff import write_tiff
import numpy as np


def apply_water_mask_tile(tile_list, in_tile_folder, out_folder, mask_file):
    for til in tile_list:
        # set folder path
        folder_in_tile = os.path.join(in_tile_folder, til)
        if not os.path.exists(folder_in_tile):
            raise Warning("In folder tile doesn't exist")
        outfolder_tile = os.path.join(out_folder, til)

        # create output folder if it doesn't exist
        if not os.path.exists(outfolder_tile):
            os.makedirs(outfolder_tile)

        # read mask file
        mask_arr, mask_tag = read_tiff(mask_file)


        # find all tif ssm file in C01 folder, add to  list
        ssm_list = os.listdir(folder_in_tile)

        # go through the loop of ssm tif files in list
        for ssmfile in ssm_list:
            if ssmfile[19:28] == "SSM------":
                ssm_arr, ssm_arr_tag = read_tiff(os.path.join(folder_in_tile, ssmfile))
                 # mask
                mask = (mask_arr == 255)
                ssm_arr[mask] = 255
                print np.amin(ssm_arr), np.amax(ssm_arr)
                # write to file
                # ct = gdal.ColorTable()
                # ct.SetColorEntry(0, (0, 0, 0, 255))
                # ct.SetColorEntry(1, (0, 255, 0, 255))
                # ct.SetColorEntry(2, (255, 0, 0, 255))
                # ct.SetColorEntry(3, (255, 0, 255, 255))
                write_tiff(os.path.join(outfolder_tile, ssmfile), src_arr=ssm_arr, tags_dict=ssm_arr_tag)
                # pyplot.imsave(os.path.join(outfolder_tile, ssmfile.replace("SSM------", "SSMANOM--")), image_arr)
        print "SSM Anomaly processed for ", til


if __name__ == "__main__":
    # test with:
    # tile list:
    # folder B02: /eodc/private/tuwgeo/users/tle/eopdanube/datapool_proc_testssm
    # folder C01
    # outfolder

    apply_water_mask_tile(tile_list=["E036N018T6"],
                          in_tile_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Envisat_ASAR/WS/products/datasets/ssm/C0102/EQUI7_EU500M",
                          out_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/walther_request",
                          mask_file="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/walther_request/water_mask/EU075M_E036N018T6_2010lc030.tif")

    # apply_water_mask_tile(tile_list=["E036N006T6", "E036N012T6", "E036N018T6", "E036N024T6", "E036N030T6"],
    #                       folderB02="/eodc/private/tuwgeo/users/tle/eopdanube/datapool_proc_testssm/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU500M/",
    #                       folderC01="/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm/C0102/EQUI7_EU500M/",
    #                       outfolder="/eodc/private/tuwgeo/users/tle/eopdanube/datapool_proc_testssm/sm_anomaly9/")
