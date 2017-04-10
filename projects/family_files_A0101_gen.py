'''
export all open layers in Qgis into a text file
also export all related-files of open layers into a different text file
use for sgrt tile
'''

import sys, os, fnmatch




def family_list_gen(list_source_file=''):
    with open(list_source_file) as f:
        lines = f.read().splitlines()

    tf_full = open(list_source_file + "_tobe_removed", 'w')

    for fil in lines:
        path, filename = os.path.split(fil)
        for file in fnmatch.filter(os.listdir(path), (filename[:16] + "*.tif")):
            tf_full.write(path + os.sep + file + '\n')
    tf_full.close()

if __name__ =="__main__":
    family_list_gen("/eodc/private/tuwgeo/users/radar/projects_work/Copernicus_HRLs/data_processing_status/final_list/final_list_clean_and_blackEdge/final_list_artifacts_tle/E061N036T1")