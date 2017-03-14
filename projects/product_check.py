
import os, fnmatch


def check_product(in_big_folder=None, products=[], outfile=None):
    '''
    Check the whole  product folder, write processed tile into file
    :param in_big_folder:
    :param products:
    :param outfile:
    :return:
    '''

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
    # list all subfolder in this folder
    for tile_folder in fnmatch.filter([x[0] for x in os.walk(in_big_folder)], '*/E*N*T*'):
        # filter to get tile folder
        if not (tile_folder[-2:].isalpha() or tile_folder[-10:-8].isalpha()):  # TODO: add a better filter
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
        fl = open(outfile, 'a')
        fl.write('%s\n' % (folder))

def check_complete_product(list_file=None, src_wf=None, target_wf=None, branch='D'):

    with open(list_file) as f:
        tile_list = f.read().splitlines()

    if src_wf == 'A0101pool':
        src_folder = "/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/preprocessed/datasets/resampled/A0101/EQUI7_EU010M"
        src_filter = "*SIG*VV"
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

    if target_wf == 'A0101pool':
        target_folder = "/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/preprocessed/datasets/resampled/A0101/EQUI7_EU010M"
        target_filter = "*SIG*VV"
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


    list02 = '/eodc/private/tuwgeo/users/radar/projects_work/Copernicus_HRLs/data_processing_status/tile_list_002.txt'
    list02plus = '/eodc/private/tuwgeo/users/radar/projects_work/Copernicus_HRLs/data_processing_status/tile_list_002_plus.txt'

    for target_wf in ['C0701draft', 'C0201draft', 'C0102draft']:
        check_complete_product(list_file=list02plus,
                               src_wf='A0101draft',
                               target_wf=target_wf,
                               branch='D')
