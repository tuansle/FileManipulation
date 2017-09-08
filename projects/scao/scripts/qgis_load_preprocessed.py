import os
import glob
from qgis.core import QgsRasterLayer
from qgis.core import QgsMapLayerRegistry
from PyQt4.QtCore import QFileInfo

tiles = ["E035N024T1",
         "E035N025T1",
         "E036N025T1",
         "E037N024T1",
         "E040N021T1",
         "E048N023T1",
         "E049N023T1"]

in_path = r"/eodc/private/tuwgeo/datapool_processed/Sentinel-1_CSAR/IWGRDH/preprocessed/datasets/resampled/A0101/EQUI7_EU010M"

rootGroup = iface.layerTreeView().layerTreeModel().rootGroup()
testGroup = rootGroup.addGroup("param")
for tilename in tiles:
    tile_path = os.path.join(in_path, tilename) + os.sep + 'qlooks'
    var_ids = ["SIG0"]
    tileGroup = testGroup.addGroup(tilename)

    # add dry,wet,water layers
    for varName in var_ids:

        fnames = glob.glob(os.path.join(tile_path, "*{}*VV*.tif".format(varName)))
        for fname in fnames:
            fileInfo = QFileInfo(fname)
            baseName = fileInfo.baseName()
            rlayer = QgsRasterLayer(fname, baseName)
            if not rlayer.isValid():
                print "Failed to load: {}".format(baseName)
            else:
                QgsMapLayerRegistry.instance().addMapLayer(rlayer, False)
                tileGroup.addLayer(rlayer)
print "Done!"
