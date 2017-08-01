import os
from sgrt.common.formats.geotiff.read_tiff import read_tiff
from sgrt.common.formats.geotiff.write_tiff import write_tiff
import numpy as np
from osgeo import gdal
import scipy.ndimage
from sgrt.common.utils.colortable import ColorTable
from sgrt.common.utils.colortable import get_gdal_ct


def apply_water_mask_tile(tile_list, in_tile_folder, out_folder, mask_folder):
    # create outfolder if it doesn't exist
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    for til in tile_list:
        # set folder path
        folder_in_tile = os.path.join(in_tile_folder, til)
        if not os.path.exists(folder_in_tile):
            raise Warning("In folder tile doesn't exist")
        outfolder_tile = os.path.join(out_folder, til)

        # create output folder if it doesn't exist
        if not os.path.exists(outfolder_tile):
            os.makedirs(outfolder_tile)

        # choose the right mask
        mask_list = os.listdir(mask_folder)
        for mask_file in mask_list:
            if til in mask_file:
                # read mask file
                mask_arr, mask_tag = read_tiff(os.path.join(mask_folder,mask_file))
                mask_resampled = scipy.ndimage.zoom(mask_arr, 0.15, order=3)

        # find all tif ssm file in C01 folder, add to  list
        ssm_list = os.listdir(folder_in_tile)

        # go through the loop of ssm tif files in list
        for ssmfile in ssm_list:
            if ssmfile[19:28] == "SSM------":
                try:
                    ssm_arr, ssm_arr_tag = read_tiff(os.path.join(folder_in_tile, ssmfile))
                except:
                    print ssmfile, "read error"
                    continue

                # mask
                mask = (mask_resampled == 255)
                try:
                    ssm_arr[mask] = 255
                except:
                    print ssmfile, "mask error"
                    continue

                # write to file
                # ct = gdal.ColorTable()
                # ct.SetColorEntry(0, (0, 0, 0, 255))
                # ct.SetColorEntry(1, (0, 255, 0, 255))
                # ct.SetColorEntry(2, (255, 0, 0, 255))
                # ct.SetColorEntry(3, (255, 0, 255, 255))
                col = ColorTable()
                ct = get_gdal_ct("sgrt_ct_cont_ssm")
                write_tiff(os.path.join(outfolder_tile, ssmfile), src_arr=ssm_arr, tags_dict=ssm_arr_tag, ct=ct)

        print "Water masking processed for ", til


if __name__ == "__main__":
    # test with:
    # tile list:
    # folder B02: /eodc/private/tuwgeo/users/tle/eopdanube/datapool_proc_testssm
    # folder C01
    # outfolder
    # apply_water_mask_tile(tile_list=["E036N018T6"],
    #                       in_tile_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Envisat_ASAR/WS/products/datasets/ssm/C0102/EQUI7_EU500M",
    #                       out_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/walther_request",
    #                       mask_file="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/walther_request/water_mask/EU075M_E036N018T6_2010lc030.tif")

    apply_water_mask_tile(tile_list=["E042N018T6", "E042N012T6", "E048N006T6" , "E048N012T6", "E048N018T6", "E048N024T6", "E054N006T6", "E054N012T6",
"E054N018T6",
"E060N006T6",
"E060N012T6", "E060N018T6"   ],
                          in_tile_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube/Envisat_ASAR/WS/products/datasets/ssm/C0102/EQUI7_EU500M",
                          out_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft_eopdanube_masked/Envisat_ASAR/WS/products/datasets/ssm/C0102/EQUI7_EU500M",
                          mask_folder="/eodc/private/tuwgeo/datapool_processed/GLC30/dataset/EQUI7_EU075M/")

    # apply_water_mask_tile(tile_list=["E036N006T6", "E036N012T6", "E036N018T6", "E036N024T6", "E036N030T6"],
    #                       folderB02="/eodc/private/tuwgeo/users/tle/eopdanube/datapool_proc_testssm/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU500M/",
    #                       folderC01="/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm/C0102/EQUI7_EU500M/",
    #                       outfolder="/eodc/private/tuwgeo/users/tle/eopdanube/datapool_proc_testssm/sm_anomaly9/")