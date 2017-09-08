import os, sys
import fnmatch
import glob
import numpy as np
from qgis.core import QgsRasterLayer
from qgis.core import QgsMapLayerRegistry
from PyQt4.QtCore import QFileInfo

sites = [#"100kmE28N17", 
         "100kmE35N38",
         #"100kmE38N30",
         "100kmE44N23",
         #"100kmE45N33",
         #"100kmE48N27"

         #"100kmE45N39",
         #"100kmE47N50",
         #"100kmE51N43"
        ]

in_path = r"/eodc/private/tuwgeo/VSC/users/scao/Copernicus_HRLs/products/S1AIW/prepare4delivery/2016-11-28_update/wetness"

rootGroup = iface.layerTreeView().layerTreeModel().rootGroup()

for sitename in sites:
    site_path = os.path.join(in_path, sitename)
    var_ids = ["NUMOB", "DRY40", "WET40", "FLDFQ", "SENS40"]
    siteGroup = rootGroup.addGroup(sitename)

    # add dry,wet,water layers
    for varName in var_ids:
        varGroup = siteGroup.addGroup(varName.lower())

        fnames= sorted(glob.glob(os.path.join(site_path, "*{}*.tif".format(varName))))
        for fname in fnames: 
            fileInfo = QFileInfo(fname)
            baseName = fileInfo.baseName()
            rlayer = QgsRasterLayer(fname, baseName)
            if not rlayer.isValid():
                print "Failed to load: {}".format(baseName)
            else:
                QgsMapLayerRegistry.instance().addMapLayer(rlayer, False)
                varGroup.addLayer(rlayer)
print "Done!"
        
