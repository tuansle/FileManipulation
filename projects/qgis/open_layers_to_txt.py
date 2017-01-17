'''
export all open layers in Qgis into a text file
also export all related-files of open layers into a different text file
use for sgrt tile
'''

import sys, os, fnmatch
cwd = "/home/tle/code/mine/FileManipulation/projects/qgis/"
sys.path.append(cwd)


# out folder
OutFolder = '%s/temp' % cwd
# if not exist, create output folder
if not os.path.exists(OutFolder):
    os.makedirs(OutFolder)
# open file for writing
tf = open(OutFolder + os.sep + "current_open_layer.txt", 'w')
tf_full = open(OutFolder + os.sep + "current_open_layer_toberemoved.txt", 'w')

# loop through open layers
for lyr in QgsMapLayerRegistry.instance().mapLayers().values():
    # write open layers to file
    tf.write("%s\n" % lyr.source())
    # take all file which correspond to the file above
    path, filename = os.path.split(lyr.source())
    for file in fnmatch.filter(os.listdir(path), (filename[:-57] + "*.tif")):
        tf_full.write(path + os.sep + file + '\n')
tf.close()
tf_full.close()

