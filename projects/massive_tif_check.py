import multiprocessing as mp
from osgeo import gdal
from PIL import Image
import os, fnmatch
import datetime

def tif_check(tile_folder, out_folder=None, user='tle', des=''):
    '''
    check one tif file by opening it (using gdal and PIL Image).
    :param tile_folder: path to tif tile folder
    :return: a text file which is a list of problematic files
    '''
    error_file_list = []

    # get all tif file in this folder, started with M* or D*, do the loop
    tif_list = (fnmatch.filter(os.listdir(tile_folder), 'M*.tif') + fnmatch.filter(os.listdir(tile_folder), 'D*.tif'))
    for filename in tif_list:
        # try to open by gdal
        fullpath = os.path.join(tile_folder, filename)
        tf = gdal.Open(fullpath)
        # catch error file
        # if error, add file to error_file_list, set status = 0, continue the loop
        if tf == None:
            error_file_list.append(fullpath)
        else:
            # try to open by Image
            # catch error file
            try:
                im = Image.open(fullpath)
            # if error, add file to error_file_list
            except IOError:
                error_file_list.append(fullpath)

    # define outfolder
    # time
    time = datetime.date.today().isoformat()
    # assing output directory. If it doesn't exist, create new folder
    if out_folder == None:
        cwd = os.path.dirname(os.path.realpath(__file__))
        OutFolder = '%s/temp' % cwd
        if not os.path.exists(OutFolder):
            os.makedirs(OutFolder)

    if error_file_list:
        # create filenames
        # ---- when adding new table, specify the new update file here ----
        outfileR = OutFolder + os.sep + 'resampled_%s_%s_%s' %(time, user, des) # resampled data
        outfileR_remove = OutFolder + os.sep + 'remove_resampled_%s_%s_%s' %(time, user, des) # resampled data
        outfileTC = OutFolder + os.sep + 'tcomposites_%s_%s_%s' %(time, user, des) # temporal composites
        outfileTC_remove = OutFolder + os.sep + 'remove_tcomposites_%s_%s_%s' %(time, user, des) # temporal composites
        outfileP = OutFolder + os.sep + 'parameters_%s_%s_%s' %(time, user, des) # parameters
        outfileP_remove = OutFolder + os.sep + 'remove_parameters_%s_%s_%s' %(time, user, des) # parameters
        outfileW = OutFolder + os.sep + 'water_%s_%s_%s' %(time, user, des) # water
        outfileW_remove = OutFolder + os.sep + 'remove_water_%s_%s_%s' %(time, user, des) # water
        outfileSSM = OutFolder + os.sep + 'ssm_%s_%s_%s' %(time, user, des) # surface soil moisture
        outfileSSM_remove = OutFolder + os.sep + 'remove_ssm_%s_%s_%s' %(time, user, des) # surface soil moisture

        # define outfile
        if tile_folder[-39:-30] == 'resampled' and tile_folder[-61:-49] == 'preprocessed':
            of = open(outfileR, 'w')
            for item in error_file_list:
                of.write(item + '\n')
            of.close()

            # write full list of files to be removed
            of = open(outfileR_remove, 'w')
            for item in error_file_list:
                for file in fnmatch.filter(tif_list, (os.path.basename(item)[:-57]+"*.tif")):
                    of.write(tile_folder+os.sep+file + '\n')
            of.close()

        elif tile_folder[-41:-30] == 'tcomposites' and tile_folder[-59:-51] == 'products':
            of = open(outfileTC, 'w')
            for item in error_file_list:
                of.write(item + '\n')
            of.close()

            # write full list of files to be removed
            of = open(outfileTC_remove, 'w')
            for item in error_file_list:
                for file in fnmatch.filter(tif_list, (os.path.basename(item)[:-57] + "*.tif")):
                    of.write(tile_folder + os.sep + file + '\n')
            of.close()

        elif tile_folder[-38:-30] == 'par_sgrt' and tile_folder[-58:-48] == 'parameters':
            of = open(outfileP, 'w')
            for item in error_file_list:
                of.write(item + '\n')
            of.close()

            # write full list of files to be removed
            of = open(outfileP_remove, 'w')
            for item in error_file_list:
                for file in fnmatch.filter(tif_list, (os.path.basename(item)[:-57] + "*.tif")):
                    of.write(tile_folder + os.sep + file + '\n')
            of.close()

        elif tile_folder[-35:-30] == 'water' and tile_folder[-53:-45] == 'products':
            of = open(outfileW, 'w')
            for item in error_file_list:
                of.write(item + '\n')
            of.close()

            # write full list of files to be removed
            of = open(outfileW_remove, 'w')
            for item in error_file_list:
                for file in fnmatch.filter(tif_list, (os.path.basename(item)[:-57] + "*.tif")):
                    of.write(tile_folder + os.sep + file + '\n')
            of.close()

        elif tile_folder[-33:-30] == 'ssm' and tile_folder[-51:-43] == 'products':
            of = open(outfileSSM, 'w')
            for item in error_file_list:
                of.write(item+'\n')
            of.close()

            # write full list of files to be removed
            of = open(outfileSSM_remove, 'w')
            for item in error_file_list:
                for file in fnmatch.filter(tif_list, (os.path.basename(item)[:-57] + "*.tif")):
                    of.write(tile_folder + os.sep + file + '\n')
            of.close()

        else:
            out_err_folder = OutFolder + os.sep + 'folder_error_%s_%s_%s' % (time, user, des)
            print "There is a problem with ", tile_folder
            # write error folder to file
            of = open(out_err_folder, 'w')
            of.write(tile_folder+'\n')
            of.close()

    if tif_list == []:
        out_nofile_folder = OutFolder + os.sep + 'folder_nofile_%s_%s_%s' % (time, user, des)
        print "Folder ", tile_folder, "has no file inside"
        # write error folder to file
        of = open(out_nofile_folder, 'w')
        of.write(tile_folder+'\n')
        of.close()

def tif_check_mp(in_folder):
    '''
    multiprocessing implementation for tif_check
    :param in_folder:string
    it's needed to specify to tile: e.g.: /eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/preprocessed/datasets/resampled/A0101/EQUI7_AF010M/
    :return:
    '''
    # Create update files:
    # process_name = str(mp.current_process())[20]
    des = in_folder[-61:].replace(os.sep, "")

    # print "create update files for:", InFolder, "by worker:", process_name
    tif_check(tile_folder=in_folder, user='tle', des=des)

def union_output(temp_folder=None):
    # check and assign temp folder
    if temp_folder == None:
        cwd = os.path.dirname(os.path.realpath(__file__))
        temp_folder = '%s/temp' % cwd

    obj = ["folder_error", "folder_nofile", "remove_ssm_", "ssm_", "remove_water_", "water_", "remove_parameters_",
           "resampled_", "remove_resampled_", "tcomposites_", "remove_tcomposites_", "parameters_"]

    for product_type in obj:
        # open all files in each type
        all_files = []
        for file in fnmatch.filter(os.listdir(temp_folder), product_type+ "*"):
            file_full_path = temp_folder + os.sep + file
            # read file, append to list
            with open(file_full_path) as f:
                lines = f.read().splitlines()
                for line in lines:
                    all_files.append(line)
        # write to only one file
        if all_files:
            outfile_full_path = temp_folder + os.sep + "all_"+product_type
            tf = open(outfile_full_path, 'w')
            for item in all_files:
                tf.write("%s\n" % item)
            tf.close()


def tif_check_main(in_big_folder):
    '''
    get all tile folder in in_folder and through to multiprocessing pool, after that, prepare a list of error file
    need to be removed with PLIA, MASK and SIG0
    :param in_big_folder: input folder need to check tif files
    :return:
    '''
    # check output folder
    cwd = os.path.dirname(os.path.realpath(__file__))
    OutFolder = '%s/temp' % cwd
    # if not exist, create output folder
    if not os.path.exists(OutFolder):
        os.makedirs(OutFolder)

    # initiate tile folders list
    dir_list_all = []

    # list all subfolder in processed datapool,# condition to consider as a tile folder
    for tile_folder in fnmatch.filter([x[0] for x in os.walk(in_big_folder)], '*/E*N*T*'):
        # check to exclude quicklook folder
        if not (tile_folder[-2:].isalpha() or tile_folder[-10:-8].isalpha()):  # TODO: add a better filter
            dir_list_all.append(tile_folder)

    # process the list with multiprocessing pool
    pool = mp.Pool(8)
    pool.map(tif_check_mp, dir_list_all)



#tif_check_main("/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/")
#union_output()
