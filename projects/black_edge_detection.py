# Copyright (c) 2014, Vienna University of Technology (TU Wien), Department
# of Geodesy and Geoinformation (GEO).
# All rights reserved.
#
# All information contained herein is, and remains the property of Vienna
# University of Technology (TU Wien), Department of Geodesy and Geoinformation
# (GEO). The intellectual and technical concepts contained herein are
# proprietary to Vienna University of Technology (TU Wien), Department of
# Geodesy and Geoinformation (GEO). Dissemination of this information or
# reproduction of this material is forbidden unless prior written permission
# is obtained from Vienna University of Technology (TU Wien), Department of
# Geodesy and Geoinformation (GEO).

'''
Created on November 23, 2016

@author: Iftikhar Ali, iftikhar.ali@geo.tuwien.ac.at
'''




import os
import fnmatch
import numpy as np
from osgeo import gdal, gdal_array
from datetime import datetime


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_tiff(src_file, sub_rect=None):
	"""
	By Vahid N.
	Parameters
	----------
	src_file: string (required)
			The full path of source dataset.
	sub_rect : (optional)
		Set this keyword to a four-element array, [Xoffset, Yoffset, width,
		height], that specifies a rectangular region within the input raster
		to extract.

	CAUTION: the returned geotags corresponds to input file and not the
			 returned src_arr (in case sub_rect is set)
	"""
	src_data = gdal.Open(src_file)
	driver = src_data.GetDriver()
	if driver.ShortName != 'GTiff':
		raise OSError("input file is not a tiff file")

	# Fetch the number of raster bands on this dataset.
	raster_count = src_data.RasterCount
	if raster_count != 1:
		raise OSError("Current version of read_tiff function can only handle \
						1-band tif files!")

	src_band = src_data.GetRasterBand(1)
	no_data_val = src_band.GetNoDataValue()
	data_type = gdal_array.GDALTypeCodeToNumericTypeCode(src_band.DataType)

	# get parameters
	description = src_data.GetDescription()
	metadata = src_data.GetMetadata()
	# Fetch the affine transformation coefficients.
	geotransform = src_data.GetGeoTransform()
	spatialreference = src_data.GetProjection()
	gcps = src_data.GetGCPs()

	tags_dict = {'description': description,
				 'metadata': metadata,
				 'geotransform': geotransform,
				 'spatialreference': spatialreference,
				 'gcps': gcps,
				 'no_data_val': no_data_val,
				 'datatype': data_type,
				 'blockxsize': src_band.GetBlockSize()[0],
				 'blockysize': src_band.GetBlockSize()[1]}

	if sub_rect is None:
		src_arr = src_data.ReadAsArray()
	else:
		src_arr = src_data.ReadAsArray(sub_rect[0], sub_rect[1], sub_rect[2], sub_rect[3])

	src_data = None
	return src_arr, tags_dict
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Row profile analysis.
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



#sig0, sig0_tag = read_tiff("M20141018_171405--_SIG0-----_S1AIWGRDH1VHA_015_A0101_EU010M_E048N012T1.tif") #Faulty
#sig0, sig0_tag = read_tiff("M20141103_181830--_SIG0-----_S1AIWGRDH1VVA_074_A0101_EU010M_E032N009T1.tif") #Faulty
#sig0, sig0_tag = read_tiff("M20141003_182548--_SIG0-----_S1AIWGRDH1VHA_149_A0101_EU010M_E031N008T1.tif")      #Clean

s_time = datetime.utcnow()

out_path = "/eodc/private/tuwgeo/users/tle/Copernicus_HRLs/data_proc_2missing_tiles_QC/EU"
tiles_path = "/eodc/private/tuwgeo/users/tle/Copernicus_HRLs/data_proc_2missing_tiles/Sentinel-1_CSAR/IWGRDH/preprocessed/datasets/resampled/A0101/EQUI7_EU010M"

#tiles_list = tiles_list[1:]         # For mac to remove the ./ file
#sig0_file_list = fnmatch.filter(os.listdir(tiles_path),'*_SIG0*VH*.tif')
#tiles_list = os.listdir(tiles_path) # Should work in windows

## Round 1 '108' tiles:
##tiles_list = ['E030N011T1', 'E031N011T1']

in_flist = r'/eodc/private/tuwgeo/users/tle/Copernicus_HRLs/data_proc_2missing_tiles/Sentinel-1_CSAR/IWGRDH/preprocessed/datasets/resampled/A0101/EQUI7_EU010M/list_missing2tiles_EU.txt'

fnames = list()
with open(in_flist) as f:
	fnames= [x.strip() for x in f.readlines() if x.strip()]

tiles_list = fnames

'''
######################################################
------
TODO:
-----
Double the sample and set the values to:
rs <= -3500
noise >= 8

---------------------------------------------------
Soft condition: better where ocean part is involved
---------------------------------------------------
noise = (rs <= -3500).sum()
print('Number of noisy values: ', noise)
if(noise >= 4):

----------------------------------------
Hard condition: better for inland areas:
----------------------------------------
noise = (rs <= -3500).sum()
print('Number of noisy values: ', noise)
if(noise >= 10):
######################################################
'''



print('Files listing.')

for tile in range(len(tiles_list)):
	#file1 = open('{0}/{1}/{2}.txt'.format(out_path, tiles_list[tile], tiles_list[tile]), 'w')
	file1 = open(os.path.join(out_path, tiles_list[tile]+'.txt'), 'w')
	#file2 = open("{0}/{1}/summary_statistic_{2}.txt".format(tiles_path, tiles_list[tile], tiles_list[tile]), "w")
	sig0_file_list = fnmatch.filter(os.listdir(tiles_path + '/' + tiles_list[tile]), '*_SIG0*VV*.tif')
	for sig0_file in range(len(sig0_file_list)):
		try:
			sig0, sig0_tag = read_tiff(tiles_path + '/' + tiles_list[tile] + '/' + sig0_file_list[sig0_file])
			samples = np.linspace(0, 10000, num=400, endpoint=False)
			row_dict = {}
			col_dict = {}
			for x in range(len(samples)):
				row_dict["row_s{0}".format(x)] = sig0[int(round(samples[x])), :]
				col_dict["col_s{0}".format(x)] = sig0[:, int(round(samples[x]))]

			empty_score_row = 0
			bad_score_row = 0
			row_noise_arr = []
			for k, v in row_dict.items():
				rs = v
				if(all(x==rs[0] for x in rs) == True):
					empty_score_row = empty_score_row + 1
				else:
					mask = rs[:] != -9999
					rs = rs[mask]
					#plt.plot(range(len(rs)), rs)
					noise = (rs <= -3450).sum()
					#print('Number of noisy values: ', noise)
					if(noise >= 4):
						bad_score_row = bad_score_row + 1
						row_noise_arr.append(noise)
					else:
						pass
						#print globals()['row_s'+str(s+1)], "is a clean sample."

			# plt.axhline(y=-2800, xmin=0, xmax=9999, hold=None, color='r')
			# plt.axhline(y=-3500, xmin=0, xmax=9999, hold=None, color='g')
			# plt.ylim( -12000, 0 )
			# plt.title("Profiles after masking.")
			#print('row_noise_arr: ', row_noise_arr)
			#plt.show()

			#print '======== Good_score_row: ', empty_score_row
			#print '======== Bad_score_row: ', bad_score_row


	#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	# Column profile analysis.
	#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
			#plt.subplot(223)
			#for j in range(19):
				#plt.plot(range(10000), globals()['col_s'+str(j+1)])
			#plt.axhline(y=-2800, xmin=0, xmax=9999, hold=None, color='r')
			#plt.axhline(y=-3500, xmin=0, xmax=9999, hold=None, color='g')
			#plt.ylim( -12000, 0 )
			#plt.xlabel('Number of pixels in transect.')
			#plt.ylabel('(SIG0 [dB])*100 \n Vertical')
			#plt.show()
			#print "Done...."

			#plt.subplot(224)
			empty_score_col = 0
			bad_score_col = 0
			col_noise_arr = []
			for k, v in col_dict.items():
				rs = v
				if(all(x==rs[0] for x in rs) == True):
					empty_score_col = empty_score_col + 1
				else:
					mask = rs[:] != -9999
					rs = rs[mask]
					#plt.plot(range(len(rs)), rs)
					noise = (rs <= -3450).sum()
					#print('Number of noisy values: ', noise)
					if (noise >= 4):
						bad_score_col = bad_score_col + 1
						col_noise_arr.append(noise)
					else:
						pass
						#print globals()['row_s' + str(s + 1)], "is a clean sample."


			# plt.axhline(y=-2800, xmin=0, xmax=9999, hold=None, color='r')
			# plt.axhline(y=-3500, xmin=0, xmax=9999, hold=None, color='g')
			# plt.ylim( -12000, 0 )
			# plt.xlabel('Number of pixels in transect.')
			# print('col_noise_arr: ', col_noise_arr)
			# plt.show()

			#print '======== Good_score_col: ', empty_score_col
			#print '======== Bad_score_col: ', bad_score_col

			if ( (bad_score_row or bad_score_col) >= 1):
				file1.write("{}/{}/{}\n".format(tiles_path, tiles_list[tile], sig0_file_list[sig0_file]))
				#file1.write("{0}\n".format(sig0_file_list[sig0_file]))
				# Basic statistics:
				#err_percent = (bad_score_col/len(sig0_file_list))*100
				#file2.write("Tile number: {0} \n Total number of files in this tile: {1} \n Number of faulty scenes: {2} \n Error percent: {3} \n".format(tiles_list[tile],
				#                                                                                                                                        len(sig0_file_list),
				#                                                                                                                                         bad_score_col,
				#                                                                                                                                        err_percent))
			else:
				pass
				#print('Clean file.')
				#os.remove(tiles_list[tile]+".txt")
				#os.remove(tiles_path +'/'+ tiles_list[tile] + '/' + tiles_list[tile] + '.txt')
		except:
			print 'Not a supported file format.'

		print '##### Tiles: ===> ({}/{}) ##### Files: ===> ({}/{}) #####'.format(tile+1, len(tiles_list), sig0_file+1, len(sig0_file_list))
	#print 'Tile ==========> {}/{} <=========='.format(tile, len(tiles_list))

file1.close()
#file2.close()
print "<<< Process Complete >>>"

e_time = datetime.utcnow()
print "calculation time: " + str((e_time - s_time).total_seconds())

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

