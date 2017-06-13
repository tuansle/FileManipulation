import os



def get_filelist(dir):
    filelist = []

    for path, subdirs, files in os.walk(dir):
        for filename in files:
            filelist.append(os.path.join(path,filename))


    # write list to file
    tf = open('file_in_directory.txt', 'w')

    for item in filelist:
        tf.write("%s\n" % item)

    tf.close()

if __name__ == "__main__":
    get_filelist("/eodc/private/tuwgeo/envisat/Datapool_raw/ASAR")