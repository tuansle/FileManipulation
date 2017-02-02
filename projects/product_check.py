
import os, fnmatch


def check_product(in_big_folder=None, products=[], outfile=None):

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
            for filename in tif_list:
                if filename[19:28] in product_formatted:
                    outfolder_list.append(tile_folder)
                    break

    # write to file
    if outfile == None:
        cwd = os.path.dirname(os.path.realpath(__file__))
        OutFolder = '%s/temp' % cwd
        if not os.path.exists(OutFolder):
            os.makedirs(OutFolder)

    #write to file, really
    outfile = os.path.join(OutFolder, 'check_product_success.txt')
    fl = open(outfile)
    for folder in outfolder_list:
        fl = open(outfile, 'a')
        fl.write('%s\n' % (folder))



check_product(in_big_folder="/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU010M/", products=['tmenplia'])

