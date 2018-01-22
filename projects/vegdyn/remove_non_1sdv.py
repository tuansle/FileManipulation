import os, shutil


def remove_non_1sdv(in_path, out_path, textfile):
    '''
    to move all processed files in directory based on a provided list of raw files to a new directory

    Parameters
    ----------
    in_path: path to preprocessed folder
    outpath: path to move affected files
    textfile: filelist for raw files

    Returns
    -------

    '''

    # open raw file list
    with open(textfile, "r") as ins:
        array = []
        for line in ins:
            # append timeframe in this format D+*date*+"_"+"time"
            array.append("D" + line[74:82] + "_" + line[83:89])

            # loop through path and delete file which start with characters in array
        for root, dirnames, filenames in os.walk(in_path):
            for filename in filenames:
                if filename[:16] in array:
                    print "moving file", os.path.join(root, filename)
                    shutil.move(os.path.join(root, filename), os.path.join(out_path, filename))


if __name__ == "__main__":
    remove_non_1sdv(in_path="/home/tle/temp/testcode",
                    out_path="/home/tle/temp/testcode2",
                    textfile="/home/tle/code/filesman/projects/temp/20180101_test_sites_del.txt")
