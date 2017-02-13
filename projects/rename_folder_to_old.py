import os

folder_lists = ['test1', 'test2']
tile_lists = ['test1', 'test2']

for folder in folder_lists:
    for tile in tile_lists:
        # change tile name in folder name to old
        tile_path = os.path.join(folder,tile)
        if os.path.isdir(tile_path):
            os.rename(tile_path, tile_path + '_old')
            print tile_path, "renamed to 'old'"
        else:
            print "there is no", tile, "in", folder
