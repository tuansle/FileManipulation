import os

def text_dif_intersect(file1, file2):
    words1 = set(open(file1).read().split())
    words2 = set(open(file2).read().split())

    duplicates  = sorted(words1.intersection(words2))
    w1_dif_w2 = sorted(words1.difference(words2))
    w2_dif_w1 = sorted(words2.difference(words1))
    uniques = sorted(words1.difference(words2).union(words2.difference(words1)))


    print "Duplicates(%d):%s"%(len(duplicates),duplicates)
    print "\nUniques(%d):%s"%(len(uniques),uniques)


    cwd = os.path.dirname(os.path.realpath(__file__))
    OutFolder = '%s/temp' % cwd
    if not os.path.exists(OutFolder):
        os.makedirs(OutFolder)

    # write to file, really
    outfile_dup = os.path.join(OutFolder, 'outfile_dup.txt')
    outfile_file1_dif_file2 = os.path.join(OutFolder, 'dif_belong_to_file1.txt')
    outfile_file2_dif_file1 = os.path.join(OutFolder, 'dif_belong_to_file2.txt')

    fl = open(outfile_dup, 'w')
    for folder in duplicates:
        fl = open(outfile_dup, 'a')
        fl.write('%s\n' % (folder))

    fl = open(outfile_file1_dif_file2, 'w')
    for folder in w1_dif_w2:
        fl = open(outfile_file1_dif_file2, 'a')
        fl.write('%s\n' % (folder))

    fl = open(outfile_file2_dif_file1, 'w')
    for folder in w2_dif_w1:
        fl = open(outfile_file2_dif_file1, 'a')
        fl.write('%s\n' % (folder))


file1 = "/workdir/projects/Copernicus_HRL/data_proc_status/vahids_structure/tile_list_failing_wflows/tile_list_004_failing_A01_raw_files_list_to_be_processed_6595_files.txt"
file2 = "/workdir/projects/Copernicus_HRL/data_proc_status/vahids_structure/tile_list_failing_wflows/forStefano/EX5_S1_processednon_processed.txt"

text_dif_intersect(file1,file2)

