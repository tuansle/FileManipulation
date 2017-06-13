import os
from sgrt.common.formats.geotiff.read_tiff import read_tiff
from sgrt.common.formats.geotiff.write_tiff import write_tiff
from osgeo import gdal
import numpy as np
from matplotlib import pyplot

def calc_ssm_anomaly(tile_list,folderB02,folderC01,outfolder):
    for til in tile_list:
        # set folder path
        folderB02_tile = os.path.join(folderB02, til)
        folderC01_tile = os.path.join(folderC01, til)
        if not os.path.exists(folderB02) or not os.path.exists(folderC01):
            raise Warning("Can't find parameter or ssm folder")
        outfolder_tile = os.path.join(outfolder, til)

        #create folder if it doesn't exist
        if not os.path.exists(outfolder_tile):
            os.makedirs(outfolder_tile)


        # find mean and sdv ssm in B02 folder, if there are two images, raise an error
        for fil in os.listdir(folderB02_tile):
            if fil[19:28] == "TSTDSSM--":
                stdssm_arr, stdssm_arr_tag = read_tiff(os.path.join(folderB02_tile,fil))
            elif fil[19:28] == "TMENSSM--":
                menssm_arr, menssm_arr_tag = read_tiff(os.path.join(folderB02_tile,fil))

        # change type
        stdssm_arr = stdssm_arr.astype(np.int32)
        menssm_arr = menssm_arr.astype(np.int32)

        # find all tif ssm file in C01 folder, add to  list
        ssm_list = os.listdir(folderC01_tile)

        # go through the loop of ssm tif files in list
        for ssmfile in ssm_list:
            if ssmfile[19:28] == "SSM------":
                ssm_arr, ssm_arr_tag = read_tiff(os.path.join(folderC01_tile,ssmfile))
                ssm_arr_tag['datatype'] = np.int32
                # print ssm_arr_tag
                ssm_arr = ssm_arr.astype(np.int32)
                # calculate sm anomaly
                # print ssm_arr
                # print "minmax", np.amin(ssm_arr), np.amax(ssm_arr)
                # print "ssm 600", ssm_arr[600,600], "ssmmen 600", menssm_arr[600,600]
                image_arr = (ssm_arr - menssm_arr) / stdssm_arr
                # print "out 600", image_arr[600,600]
                print "ssm", ssm_arr[600,600], "men", menssm_arr[600,600], "result", image_arr[600,600]
                # mask
                mask = (ssm_arr == 255)
                image_arr[mask] = 255
                print np.amin(image_arr), np.amax(image_arr)
                # write to file
                # ct = gdal.ColorTable()
                # ct.SetColorEntry(0, (0, 0, 0, 255))
                # ct.SetColorEntry(1, (0, 255, 0, 255))
                # ct.SetColorEntry(2, (255, 0, 0, 255))
                # ct.SetColorEntry(3, (255, 0, 255, 255))
                write_tiff(os.path.join(outfolder_tile, ssmfile.replace("SSM------", "SSMANOM--")), src_arr=image_arr, tags_dict=ssm_arr_tag)
                # pyplot.imsave(os.path.join(outfolder_tile, ssmfile.replace("SSM------", "SSMANOM--")), image_arr)
        print "SSM Anomaly processed for ", til

if __name__ == "__main__":
    #test with:
    #tile list:
    # folder B02: /eodc/private/tuwgeo/users/tle/eopdanube/datapool_proc_testssm
    # folder C01
    # outfolder

    calc_ssm_anomaly(tile_list=["E036N006T6", "E036N012T6", "E036N018T6" , "E036N024T6", "E036N030T6" ],
                     folderB02="/eodc/private/tuwgeo/users/tle/eopdanube/datapool_proc_testssm/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU500M/",
                     folderC01="/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm/C0102/EQUI7_EU500M/",
                     outfolder="/eodc/private/tuwgeo/users/tle/eopdanube/datapool_proc_testssm/sm_anomaly9/")


