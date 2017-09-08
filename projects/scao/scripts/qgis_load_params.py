import os, sys
import fnmatch
import glob
import numpy as np
from qgis.core import QgsRasterLayer
from qgis.core import QgsMapLayerRegistry
from PyQt4.QtCore import QFileInfo

tiles = ["E029N009T1",
"E029N010T1",
"E029N011T1",
"E030N009T1",
"E030N010T1",
"E030N011T1",
"E030N012T1",
"E030N013T1",
"E031N007T1",
"E031N008T1",
"E031N009T1",
"E031N010T1",
"E031N011T1",
"E031N013T1",
"E031N014T1",
"E031N015T1",
"E031N016T1",
"E032N007T1",
"E032N008T1",
"E032N009T1",
"E032N010T1",
"E032N011T1",
"E032N012T1",
"E032N013T1",
"E032N014T1",
"E032N015T1",
"E032N016T1",
"E033N007T1",
"E033N008T1",
"E033N009T1",
"E033N010T1",
"E033N011T1",
"E033N012T1",
"E033N013T1",
"E033N014T1",
"E033N015T1",
"E033N016T1",
"E034N007T1",
"E034N008T1",
"E034N009T1",
"E034N010T1",
"E034N011T1",
"E034N012T1",
"E034N013T1",
"E034N014T1",
"E034N015T1",
"E035N007T1",
"E035N008T1",
"E035N009T1",
"E035N010T1",
"E035N011T1",
"E035N012T1",
"E035N013T1",
"E035N014T1",
"E035N015T1",
"E036N007T1",
"E036N008T1",
"E036N009T1",
"E036N010T1",
"E036N011T1",
"E036N012T1",
"E036N013T1",
"E036N014T1",
"E037N008T1",
"E037N009T1",
"E037N010T1",
"E037N011T1",
"E037N012T1",
"E037N013T1",
"E038N008T1",
"E038N010T1",
"E038N011T1",
"E038N012T1",
"E038N013T1",
"E038N014T1",
"E038N015T1",
"E038N017T1",
"E039N008T1",
"E039N009T1",
"E039N010T1",
"E039N011T1",
"E039N012T1",
"E039N013T1",
"E039N014T1",
"E039N015T1",
"E039N016T1",
"E039N017T1",
"E040N008T1",
"E040N009T1",
"E040N010T1",
"E040N011T1",
"E040N012T1",
"E040N014T1",
"E040N016T1",
"E040N017T1",
"E041N008T1",
"E041N009T1",
"E041N011T1",
"E041N012T1",
"E041N013T1",
"E041N014T1",
"E041N015T1",
"E041N016T1",
"E041N017T1"]

in_path = r"/eodc/private/tuwgeo/users/radar/datapool_processed_draft_HRLs_Spain/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU010M/"

rootGroup = iface.layerTreeView().layerTreeModel().rootGroup()
testGroup = rootGroup.addGroup("param")
for tilename in tiles:
    tile_path = os.path.join(in_path, tilename)
    var_ids = ["TMINSIG0"]
    tileGroup = testGroup.addGroup(tilename)

    # add dry,wet,water layers
    for varName in var_ids:

        fnames = glob.glob(os.path.join(tile_path, "*{}*VV*.tif".format(varName)))
        if len(fnames) == 1:
            fname = fnames[0]
            fileInfo = QFileInfo(fname)
            baseName = fileInfo.baseName()
            rlayer = QgsRasterLayer(fname, baseName)
            if not rlayer.isValid():
                print "Failed to load: {}".format(baseName)
            else:
                QgsMapLayerRegistry.instance().addMapLayer(rlayer, False)
                tileGroup.addLayer(rlayer)
print "Done!"
