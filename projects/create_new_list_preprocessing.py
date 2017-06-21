import sys, os

def create_new_list_preprocessing(src_list, preprocessed_list, dst_outfile=None):
    # from processing list and slurm output list (grep -nr slurm-5410704_* -e "pre-processed"  >processed.txt). Generate
    # new list for re-processing

    #read src_list
    with open(src_list) as f:
        src = f.read().splitlines()

    #read read pre-processed ist
    with open(preprocessed_list) as f:
        processed = f.read().splitlines()

    # new list of processed file
    processed_fullpath = []

    for i in src:
        for j in processed:
            if os.path.basename(j.split()[-1]) in i:
                processed_fullpath.append(i)

    dst_list = list(set(src_list) - set(processed_fullpath))

    if not dst_outfile:
        dst_outfile = src_list + "_reproc"

    thefile = open(dst_outfile, 'w')
    for item in dst_list:
        thefile.write("%s\n" % item)


if __name__ == "__main__":
    create_new_list_preprocessing(src_list="/home/tle/data/DATAPROCESSING/working_dir/temp/EOPDanube_S1A_Danube_T6_01102016",
                                  preprocessed_list="/home/tle/data/DATAPROCESSING/working_dir/temp/processed.txt")