import os

folder_lists = ['/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_sgrt/B0101/EQUI7_EU010M/',
                '/eodc/private/tuwgeo/users/radar/datapool_processed_draft/Sentinel-1_CSAR/IWGRDH/parameters/datasets/par_stat/B0201/EQUI7_EU010M/']


tile_lists = ['E038N009T1', 'E040N013T1', 'E040N015T1',  'E037N014T1', 'E031N012T1']

for folder in folder_lists:
    for tile in tile_lists:
        # change tile name in folder name to old
        tile_path = os.path.join(folder,tile)
        if os.path.isdir(tile_path):
            os.rename(tile_path, tile_path + '_old')
            print tile_path, "renamed to 'old'"
        else:
            print "there is no", tile, "in", folder
