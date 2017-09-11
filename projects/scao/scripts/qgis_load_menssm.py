import os, sys
import fnmatch
import glob
import numpy as np
from qgis.core import QgsRasterLayer
from qgis.core import QgsMapLayerRegistry
from PyQt4.QtCore import QFileInfo

# tiles = ["E042N018T6",
# "E042N012T6",
# "E048N006T6",
# "E048N012T6",
# "E048N018T6",
# "E048N024T6",
# "E054N006T6",
# "E054N012T6",
# "E054N018T6",
# "E060N006T6",
# "E060N012T6",
# "E060N018T6"]

in_path = r"/home/tle/data/DATAPROCESSING/eopdanube/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU500M"

rootGroup = iface.layerTreeView().layerTreeModel().rootGroup()
testGroup = rootGroup.addGroup("s1a_menssm_clima")
# for tilename in tiles:
tile_path = in_path
# var_ids = ["SSMANOM"]
# tileGroup = testGroup.addGroup(tilename)
month_group_list = []
fnames = []
# add dry,wet,water layers
for root, dirs, files in os.walk(in_path):
    for file in files:
        if file.endswith(".tif") and file.startswith('D99')  and "MMENSSM" in file:  #change to 'D99' for clima
            fnames.append(os.path.join(root, file))

print len(fnames)
if len(fnames) != 0:
    for fil in fnames:
        if os.path.basename(fil)[1:7] not in month_group_list:
            month_group_list.append(os.path.basename(fil)[1:7])


    for group in sorted(month_group_list):
        monthGroup = testGroup.addGroup(group)

    for fil in fnames:
        #find group
        monthGroup = testGroup.findGroup(os.path.basename(fil)[1:7])

        fileInfo = QFileInfo(fil)
        baseName = fileInfo.baseName()
        rlayer = QgsRasterLayer(fil, baseName)
        if not rlayer.isValid():
            print "Failed to load: {}".format(baseName)
        else:
            QgsMapLayerRegistry.instance().addMapLayer(rlayer, False)
            monthGroup.addLayer(rlayer)
print "Done!"
