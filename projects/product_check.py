
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
