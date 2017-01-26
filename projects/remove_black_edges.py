# author: Senmao Cao
import os
import shutil
import glob
from osgeo import gdal
import numpy as np
from scipy import ndimage
from osgeo.gdalconst import GA_Update
import multiprocessing as mp2

def remove_image_edges(src_arr=None, src_img_file=None, dst_img_file=None,
                       overwrite=None, pixels=None, src_nodata=None):
    '''
    Parameters
    ----------
        src_arr: image array (Numpy array) (optional)
            If not provided then src_img_file will be used.
        src_img_file: string (optional)
            The source image file name (full path).
            Ignored if src_arr is provided.
        dst_img_file: string (optional)
            Destination image file.
            Ignored if src_arr is provided.
        overwrite: string (optional)
            If True then the result will be stored in src_img_file
        pixels: scalar (optional)
            Number of pixels at edges to be removed
            Default value is pixels=1
        src_nodata: scalar (required)
            No data value of input image

    Returns
    -------
        edges-removed image array

    '''

    # check if inputarray is provided
    if src_nodata is None:
        raise ValueError('src_nodata keyword (No data value) is required!')
    # check if an image file instead of image array is provided
    if src_arr is None:
        if src_img_file is None:
            raise ValueError('src_image_file or src_arr keyword is required!')
        else:
            # check if the input image file should be overritten
            if overwrite is True:
                dst_img_file = src_img_file
            else:
                # define destination file (manipulate a copy of input image)
                if dst_img_file is None:
                    name, ex = os.path.splitext(os.path.basename(src_img_file))
                    dst_img_file = os.path.join(os.path.dirname(src_img_file),
                                                "".join((name,
                                                         '_edges_removed',
                                                         ex))
                                                )
                shutil.copyfile(src_img_file, dst_img_file)
            # open image file
            src_img = gdal.Open(dst_img_file, GA_Update)
            src_arr = np.array(src_img.ReadAsArray())

    # create a boolean mask
    mask = (src_arr == src_nodata) | (src_arr < -3300)

    # mask_not = !mask
    # create dilation structure
    struct1 = ndimage.generate_binary_structure(2, 2)
    struct1 = ndimage.morphology.iterate_structure(struct1, 5)
    # perform dilation of nodata values
    not_mask = ndimage.binary_dilation(np.logical_not(mask), structure=struct1)

    mask = np.logical_not(not_mask)

    # dilation of the mask is perform in two steps considering two different
    # disk sizes
    if pixels is None:
        pixels = 1
    # create dilation structure
    struct = ndimage.generate_binary_structure(2, 2)
    struct = ndimage.morphology.iterate_structure(struct, pixels)
    # perform dilation of nodata values
    new_mask = ndimage.binary_dilation(mask, structure=struct)

    # assign no data value based on dilated mask
    src_arr[new_mask] = src_nodata

    if src_img_file is not None:
        # write new array in destiantion file
        src_img.GetRasterBand(1).WriteArray(src_arr)

    # return dilated image array
    return src_arr

def process(filelist = None, full_path = True):
    # keep it the same
    if  full_path:
        indir = ""
        tilename = ""
    else:
        indir = r"/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/preprocessed/datasets/resampled/A0101/EQUI7_EU010M"
        tilename = os.path.basename(os.path.splitext(filelist)[0])

    tilename_out = os.path.basename(os.path.splitext(filelist)[0])

    with open(filelist) as f:
        faulty_scenes = [os.path.join(indir, tilename, x.strip()) for x in f.readlines() if x.strip()]

        #    filelist = r"/eodc/private/tuwgeo/users/radar/projects_work/Copernicus_HRLs/quality_check_for_black_edge_ia/SCao_list_checked_by_iali/E032N016T1.txt"
        #    with open(filelist) as f:
        #        faulty_scenes = [x.strip() for x in f.readlines() if x.strip()]

    # IA: please change the output directory
    outdir = r"/eodc/private/tuwgeo/users/tle/Copernicus_HRLs/Resampled_black_edge_removal/2ndwave/1sttime/{}".format(
        tilename_out)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for idx, fname in enumerate(faulty_scenes):
        dst_file = os.path.join(outdir, os.path.basename(fname))
        remove_image_edges(src_img_file=fname, dst_img_file=dst_file, src_nodata=-9999, pixels=40)
        print filelist[-14:-4], ": => ({}/{}):".format(idx+1, len(faulty_scenes)), os.path.basename(fname)


def main(mp=True):
    filelist_list = []

    file_lists_dir = '/eodc/private/tuwgeo/users/iali/Copernicus_HRLs_iali/round2_129_tiles/round2_129_bad_tile_list/1_100_tiles/'
    for filelist in glob.glob(os.path.join(file_lists_dir,"E*N*T*.txt")):
        if os.stat(filelist).st_size != 0:
            filelist_list.append(filelist)

    print len(filelist_list), "list is going to be processed"
    if mp:
        print "multiprocessing..."
        pool = mp2.Pool(10)
        pool.map(process, filelist_list)
    else:
        for filelist in filelist_list:
            process(filelist)
    print "Done!"

if __name__ == '__main__':
    main()
