import os

folder_to_rename = '/home/tle/data/DATAPROCESSING/eopdanube_testmixssm/Envisat_ASAR/WS/products/datasets/ssm/C1002/EQUI7_EU500M/E048N012T6/'

for fil in os.listdir(folder_to_rename):
    if "S1A" in fil:
        os.rename(os.path.join(folder_to_rename,fil), os.path.join(folder_to_rename,fil.replace("S1AIWGRDH","ASAWS---M")))
