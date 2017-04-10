import os

def check_mix_dm(in_big_folder=None, temp_path=None):
    '''
    input big folder, go through every file in that folder
    :param in_big_folder:
    :param products:
    :param outfile:
    :return:
    a list with
    '''

    tempdir = temp_path

    # tiles with D
    tiles_has_D = []
    for root, dirs, files in os.walk(in_big_folder):
        file_D_in_tile = []
        for name in files:
            if name.startswith("D") and name.endswith("tif"):
                tiles_has_D.append(root)
                file_D_in_tile.append(os.path.join(root, name))
        if file_D_in_tile:
            write_to_file(file_D_in_tile, tempdir + os.sep + os.path.basename(root))
    print len(set(tiles_has_D))
    write_to_file(list(set(tiles_has_D)) , tempdir + os.sep + "tiles_with_D_inside") #

def write_to_file(list=None, outfile=None):
    # check input and output
    if not list or not outfile:
        raise IOError('write_to_file: input list and outfile must be specified.')
        return 0

    if os.path.exists(outfile):
        print 'WARNING: %s file exists, overwriting...' % outfile
    tf = open(outfile, 'w')
    for item in list:
        tf.write("%s\n" % item)
    tf.close()
    return 1


if __name__ == '__main__':
    folder_param_EU = "/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU010M"
    folder_param_OC = "/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_OC010M"
    folder_ssm = "/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm/C0102/EQUI7_EU010M"
    folder_ssm_OC = "/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm/C0102/EQUI7_OC500M"
    folder_water = "/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/water/C0201/EQUI7_EU010M"
    folder_wetness = "/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/wetness/C0701/EQUI7_EU010M"

    # current dir
    dir_path = os.path.dirname(os.path.realpath(__file__))
    temppath_param_EU = dir_path + os.sep + "temp" + os.sep + "checkD_param_EU"  # add product here
    temppath_param_OC = dir_path + os.sep + "temp" + os.sep + "checkD_param_OC"  # add product here
    temppath_ssm = dir_path + os.sep + "temp" + os.sep + "checkD_ssm_EU"  # add product here
    temppath_ssm_OC = dir_path + os.sep + "temp" + os.sep + "checkD_ssm_OC"  # add product here
    temppath_water = dir_path + os.sep + "temp" + os.sep + "checkD_water"  # add product here
    temppath_wetness = dir_path + os.sep + "temp" + os.sep + "checkD_wetness"  # add product here

    for path in [temppath_param_EU,temppath_wetness,temppath_water,temppath_ssm_OC,temppath_ssm,temppath_param_OC]:
        if not os.path.exists(path):
            os.makedirs(path)


    check_mix_dm(in_big_folder=folder_param_EU, temp_path=temppath_param_EU)
    # check_mix_dm(in_big_folder=folder_param_OC, temp_path=temppath_param_OC)
    # check_mix_dm(in_big_folder=folder_ssm, temp_path=temppath_ssm)
    # check_mix_dm(in_big_folder=folder_ssm_OC, temp_path=temppath_ssm_OC)
    # check_mix_dm(in_big_folder=folder_water, temp_path=temppath_water)
    # check_mix_dm(in_big_folder=folder_wetness, temp_path=temppath_wetness)
