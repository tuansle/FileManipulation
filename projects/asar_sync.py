import os


def asar_sync():
    # read file from pool
    with open('/home/tuan/work/TUWGEO/asar_sync/files_in_directory.txt') as f:
        files_in_pool = f.read().splitlines()


    # read file from
    with open('/home/tuan/work/TUWGEO/asar_sync/files_in_esa.txt') as f:
        files_in_esa = f.read().splitlines()


    # let's do something fun

    print len(files_in_esa), len(files_in_pool)

    # files_in_pool_10 = [os.path.basename(elem)[:10] for elem in files_in_pool]

    files_in_pool_10 = []
    for elem in files_in_pool:
        if os.path.basename(elem)[:3] == "ASA":
            files_in_pool_10.append(os.path.basename(elem))

    files_in_esa_10 = []
    for elem in files_in_esa:
        if os.path.basename(elem)[:3] == "ASA":
            files_in_esa_10.append(os.path.basename(elem))

    # print "our datapool", set(files_in_pool_10)
    # print "esa", set(files_in_esa_10)
    #
    # print "esa - pool", set(files_in_esa_10) - set(files_in_pool_10)
    # print "pool - esa", set(files_in_pool_10) - set(files_in_esa_10)
    #
    #
    # print "intersec", set(files_in_esa_10) - (set(files_in_esa_10) - set(files_in_pool_10))

    download = set(files_in_esa_10) - set(files_in_pool_10)

    print len(download)


    asa_imp_1p = []
    asa_app_1p = []
    asa_apg_1p = []
    asa_im__0c = []
    asa_ims_1p = []


    fullpath = []
    for itemesa in list(set(files_in_esa)):
        if os.path.basename(itemesa) in list(download):
            tf = open(os.path.basename(itemesa)[:9], 'a')
            tf.write("%s\n" % itemesa)

    # for item in list(download):
    #     if item[:10].lower == "asa_imp_1p":
    #         asa_imp_1p.append(item)
    #
    #     elif item[:10].lower == "asa_app_1p":
    #         asa_app_1p.append(item)
    #
    #     elif item[:10].lower == "asa_im__0c":
    #         asa_im__0c.append(item)
    #
    #     elif item[:10].lower == "asa_ims_1p":
    #         asa_ims_1p.append(item)
    #
    #     elif item[:10].lower == "asa_apg_1p":
    #         asa_apg_1p.append(item)
    #     else: print item
    #
    # print len(asa_apg_1p) + len(asa_im__0c) + len(asa_ims_1p) + len(asa_app_1p) + len(asa_imp_1p)


if __name__ == "__main__":
    asar_sync()