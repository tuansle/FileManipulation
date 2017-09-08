import os, sys
import fnmatch
import glob
import numpy as np
from qgis.core import QgsRasterLayer
from qgis.core import QgsMapLayerRegistry
from PyQt4.QtCore import QFileInfo


in_path = r"/eodc/private/tuwgeo/VSC/users/vnaeimi/Sentinel-1_CSAR/IWGRDH/products/datasets/rgb_composites/C0501/EQUI7_EU010M"

rootGroup = iface.layerTreeView().layerTreeModel().rootGroup()

files = glob.glob(os.path.join(in_path, "*/qlooks/Q*S-COMP007*.tif"))

for i, fname in enumerate(sorted(files)):
    fileInfo = QFileInfo(fname)
    baseName = fileInfo.baseName()
    rlayer = QgsRasterLayer(fname, baseName)
    if not rlayer.isValid():
        print "Failed to load: {}".format(baseName)
    else:
        QgsMapLayerRegistry.instance().addMapLayer(rlayer, False)
        rootGroup.addLayer(rlayer)
    print i

print "Done!"
        
