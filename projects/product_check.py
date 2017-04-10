
import os, fnmatch


def check_product(tile_list_file=None, in_big_folder=None, products=[], outfile=None):
    '''
    Check the whole  product folder, write processed tile into file
    :param in_big_folder:
    :param products:
    :param outfile:
    :return:
    '''

    with open(tile_list_file) as f:
        tile_list = f.read().splitlines()


    # format product
    product_formatted = []
    for product in products:
        if len(product) != 9:
            for i in range(9 - len(product)):
                product += '-'
        product = product.upper()
        product_formatted.append(product)

    # initiate outfolder_list
    outfolder_list = []
    not_proc = []
    # list all subfolder in this folder
    for tile_folder in tile_list:
        # filter to get tile folder
        tile_folder = os.path.join(in_big_folder, tile_folder)
        if not (tile_folder[-2:].isalpha() or tile_folder[-10:-8].isalpha()):  # TODO: add a better filter
            # if folder not exist, add to not proc
            if not os.path.exists(tile_folder):
                not_proc.append(os.path.basename(tile_folder))
                continue
            # go to every subfolder to check if there is any file with assigned pattern, add to list
            tif_list = (fnmatch.filter(os.listdir(tile_folder), 'M*.tif') + fnmatch.filter(os.listdir(tile_folder), 'D*.tif'))
            # create a temporary instance of product_formatted
            product_formatted_temp = list(product_formatted)

            for filename in tif_list:
                if filename[19:28] in product_formatted_temp:
                    product_formatted_temp.remove(filename[19:28])
                    if product_formatted_temp == []:
                        outfolder_list.append(tile_folder)
                        break

    # write to file
    if outfile == None:
        cwd = os.path.dirname(os.path.realpath(__file__))
        OutFolder = '%s/temp' % cwd
        if not os.path.exists(OutFolder):
            os.makedirs(OutFolder)

    #write to file, really
    outfile = os.path.join(OutFolder, in_big_folder[-28:-13].replace("/", "") + '_processed.txt')
    fl = open(outfile, 'w')
    for folder in outfolder_list:
        fl.write('%s\n' % (folder))

    # write not prc
    #write to file, really
    outfile = os.path.join(OutFolder, in_big_folder[-28:-13].replace("/", "") + '_not_proc.txt')
    fl = open(outfile, 'w')
    for folder in not_proc:
        fl.write('%s\n' % (os.path.basename(folder)))

def check_complete_product(list_file=None, src_wf=None, target_wf=None, branch='D'):

    with open(list_file) as f:
        tile_list = f.read().splitlines()

    if src_wf == 'A0101':
        src_folder = "/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/preprocessed/datasets/resampled/A0101/EQUI7_EU010M"
        src_filter = "*SIG*VV"
    elif src_wf == 'C0102':
        src_folder = '/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm/C0102/EQUI7_EU010M/'
        src_filter = branch + "*SSM--"
    elif src_wf == 'C0201':
        src_folder = '/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/water/C0201/EQUI7_EU010M/'
        src_filter = branch + "*WATER"
    elif src_wf == 'C0701':
        src_folder = '/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/wetness/C0701/EQUI7_EU010M/'
        src_filter = branch + "*WWS-"
    elif src_wf == 'A0101draft':
        src_folder = "/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/preprocessed/datasets/resampled/A0101/EQUI7_EU010M/"
        src_filter = "*SIG*VV"
    elif src_wf == 'C0102draft':
        src_folder = '/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm/C0102/EQUI7_EU010M/'
        src_filter = branch + "*SSM--"
    elif src_wf == 'C0201draft':
        src_folder = '/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/products/datasets/water/C0201/EQUI7_EU010M/'
        src_filter = branch + "*WATER"
    elif src_wf == 'C0701draft':
        src_folder = '/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/products/datasets/wetness/C0701/EQUI7_EU010M/'
        src_filter = branch + "*WWS-"

    if target_wf == 'A0101':
        target_folder = "/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/preprocessed/datasets/resampled/A0101/EQUI7_EU010M"
        target_filter = "*SIG*VV"
    elif target_wf == 'C0102':
        target_folder = '/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm/C0102/EQUI7_EU010M/'
        target_filter = branch + "*SSM--"
    elif target_wf == 'C0201':
        target_folder = '//eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/water/C0201/EQUI7_EU010M/'
        target_filter = branch + "*WATER"
    elif target_wf == 'C0701':
        target_folder = '/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/wetness/C0701/EQUI7_EU010M/'
        target_filter = branch + "*WWS-"
    elif target_wf == 'A0101draft':
        target_folder = "/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/preprocessed/datasets/resampled/A0101/EQUI7_EU010M/"
        target_filter = "*SIG*VV"
    elif target_wf == 'C0102draft':
        target_folder = '/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm/C0102/EQUI7_EU010M/'
        target_filter = branch + "*SSM--"
    elif target_wf == 'C0201draft':
        target_folder = '/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/products/datasets/water/C0201/EQUI7_EU010M/'
        target_filter = branch + "*WATER"
    elif target_wf == 'C0701draft':
        target_folder = '/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/products/datasets/wetness/C0701/EQUI7_EU010M/'
        target_filter = branch + "*WWS-"

    list_tile_complete=[]
    list_tile_notproc=[]
    list_tile_incomplete=[]
    list_tile_weird=[]
    for tile in tile_list:
        tile = tile.strip()
        list_img_src = []
        list_img_target = []
        if os.path.isdir(os.path.join(src_folder, tile)):
            for f in os.listdir(os.path.join(src_folder, tile)):
                if fnmatch.fnmatch(f, src_filter+'*.tif'):
                    list_img_src.append(f[1:17])

        if os.path.isdir(os.path.join(target_folder, tile)):
            for f in os.listdir(os.path.join(target_folder, tile)):
                if fnmatch.fnmatch(f, target_filter+'*.tif'):
                    list_img_target.append(f[1:17])

        if len(set(list_img_target)) == 0:
            list_tile_notproc.append(tile)
        elif len(set(list_img_src)-set(list_img_target)) == 0:
            if len(set(list_img_target)-set(list_img_src)) == 0:
                list_tile_complete.append(tile)
            else:
                list_tile_weird.append(tile)
        else:
            list_tile_incomplete.append(tile)

    tf = open('temp' + os.sep + src_wf + target_wf + branch +'_complete.txt', 'w')
    for item in list_tile_complete:
        tf.write("%s\n" % item)

    tf = open('temp' + os.sep + src_wf + target_wf + branch + '_notproc.txt', 'w')
    for item in list_tile_notproc:
        tf.write("%s\n" % item)

    tf = open('temp' + os.sep + src_wf + target_wf + branch + '_incomplete.txt', 'w')
    for item in list_tile_incomplete:
        tf.write("%s\n" % item)

    tf = open('temp' + os.sep + src_wf + target_wf + branch + '_weird.txt', 'w')
    for item in list_tile_weird:
        tf.write("%s\n" % item)

    tf.close()




if __name__ == "__main__":

    list01 = '/eodc/private/tuwgeo/users/radar/projects_work/Copernicus_HRLs/data_processing_status/tile_list_001.txt'
    list02 = '/eodc/private/tuwgeo/users/tle/temp/list_temp/tile_list_002.txt'
    list02plus = '/eodc/private/tuwgeo/users/tle/temp/list_temp/tile_list_002_plus.txt'

    listnew="/eodc/private/tuwgeo/users/tle/quality_check/check_missing_tile_042017/check_missing_tile_04_2017"


    #check_product(in_big_folder="/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/preprocessed/datasets/resampled/A0101/EQUI7_EU010M/", products=['MASK1','SIG0','PLIA'])
    #check_product(in_big_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/preprocessed/datasets/resampled/A0101/EQUI7_EU010M/", products=['MASK1','SIG0','PLIA'])
    #check_product(in_big_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_sgrt/B0101/EQUI7_EU010M/", products=['TMAXPLIA','TMAXSIG0','TMENSIG0','TMINPLIA','TMINSIG0','TP95SIG0','TP05SIG0'])
    #check_product(in_big_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU010M/", products=['TMAXSIG0','TMENSIG0','TMINSIG0','TSTDSIG0','TP10SIG0','TP90SIG0'])
    #check_product(in_big_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU010M/", products=['tmenplia'])
    #check_product(in_big_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/products/datasets/water/C0201/EQUI7_EU010M/", products=['water'])
    #check_product(in_big_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm/C0101/EQUI7_EU010M/", products=['ssm'])
    #check_product(in_big_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm/C0102/EQUI7_EU010M/", products=['ssm'])
    #check_product(in_big_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/products/datasets/wetness/C0701/EQUI7_EU010M/", products=['wws'])
    #check_product(in_big_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU010M/", products=['tfrqwater'])
    #check_product(in_big_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU010M/", products=['TFRQDRY','TFRQWET'])

    # check_product(tile_list_file=listnew, in_big_folder="/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/preprocessed/datasets/resampled/A0101/EQUI7_EU010M/", products=['MASK1','SIG0','PLIA'])
    # check_product(tile_list_file=listnew, in_big_folder="/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU010M/", products=['TMAXSIG0','TMENSIG0','TMINSIG0','TSTDSIG0','TP10SIG0','TP90SIG0'])
    # check_product(tile_list_file=listnew, in_big_folder="/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/water/C0201/EQUI7_EU010M/", products=['water'])
    # check_product(tile_list_file=listnew, in_big_folder="/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/ssm/C0102/EQUI7_EU010M/", products=['ssm'])
    # check_product(tile_list_file=listnew, in_big_folder="/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/products/datasets/wetness/C0701/EQUI7_EU010M/", products=['wws'])
    check_product(tile_list_file=listnew, in_big_folder="/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU010M/", products=['tfrqwater'])
    #check_product(in_big_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU010M/", products=['TFRQDRY','TFRQWET'])


    # for target_wf in ['C0701', 'C0201', 'C0102']:
    #     check_complete_product(list_file=listnew,
    #                            src_wf='A0101',
    #                            target_wf=target_wf,
    #                            branch='M')
