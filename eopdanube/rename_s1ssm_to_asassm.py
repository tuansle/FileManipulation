import os

def batch_rename(folder, dst_name="S1"):
    if dst_name == "S1":
        for fil in os.listdir(folder):
            if "_ASA" in fil:
                os.rename(os.path.join(folder, fil),
                          os.path.join(folder, fil.replace("ASAWS---M", "S1AIWGRDH")))
    elif dst_name == "ASA":
        for fil in os.listdir(folder):
            if "_S1" in fil:
                os.rename(os.path.join(folder, fil),
                          os.path.join(folder, fil.replace("S1AIWGRDH", "ASAWS---M")))
    else:
        raise Exception("dst_name should be ASA or S1")

if __name__ == "__main__":
    batch_rename(folder="/data/DATAPROCESSING/eopdanube_testmixssm/Envisat_ASAR/WS/parameters/datasets/par_stat/B0201/EQUI7_EU500M/E048N012T6/",
                 dst_name="ASA")