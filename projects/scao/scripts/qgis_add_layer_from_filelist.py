import os, sys
import fnmatch
import glob
import numpy as np
from qgis.core import QgsRasterLayer
from qgis.core import QgsMapLayerRegistry
from PyQt4.QtCore import QFileInfo

in_flist = r"/eodc/private/tuwgeo/users/radar/projects_work/Copernicus_HRLs/notes/quality_issue/E032N016T1_artefact_VV.txt"

#tiles = sorted(tile4)
rootGroup = iface.layerTreeView().layerTreeModel().rootGroup()
subGroup = rootGroup.addGroup("layers")

fnames = list()
with open(in_flist) as f:
    fnames= [x.strip() for x in f.readlines() if x.strip()]

for fname in sorted(fnames): 
    fileInfo = QFileInfo(fname)
    baseName = fileInfo.baseName()
    rlayer = QgsRasterLayer(fname, baseName)
    if not rlayer.isValid():
        print "Failed to load: {}".format(baseName)
    else:
        QgsMapLayerRegistry.instance().addMapLayer(rlayer, False)
        subGroup.addLayer(rlayer)
print "Done!"
        
