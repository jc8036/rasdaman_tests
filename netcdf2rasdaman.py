"""
Created on Wed Apr 06 14:20:14 2016

@author: admin
"""
import matplotlib.pyplot as plt
import netCDF4
import numpy as np
from osgeo import gdal
from osgeo import osr
import os
import subprocess

def readNetCDF(filePath):
    ncFile = netCDF4.Dataset(filePath)
    lon = np.array(ncFile.variables['longitude'])
    lat = np.array(ncFile.variables['latitude'])
    time_list = np.array(ncFile.variables['time'])    
    return (ncFile, lon, lat, time_list)

def writeTiff(ncFile, lon, lat, timestep_index, key, workspace):
    xmin,ymax,xmax,ymin = lon.min(),lat.min(),lon.max(),lat.max()
    nrows,ncols = len(lat),len(lon)
    xres = (xmax-xmin)/float(ncols)
    yres = (ymax-ymin)/float(nrows)
    
    vals_timestep = np.array(ncFile.variables[key][timestep_index])
    vals_timestep_adjusted = np.hstack((vals_timestep[:,(ncols/2):],vals_timestep[:,:(ncols/2)]))
    
    fileName = os.path.join(workspace,str(timestep)+'.tif')
    output_raster = gdal.GetDriverByName('GTiff').Create(fileName, ncols, nrows, 1 ,gdal.GDT_Float32)  # Open the file
    output_raster.SetGeoTransform([-180,xres,0,90,0,yres])  # Specify its coordinates
    srs = osr.SpatialReference()                 # Establish its coordinate encoding
    srs.ImportFromEPSG(4326)                     # This one specifies WGS84 lat long.
    output_raster.SetProjection( srs.ExportToWkt() )   # Exports the coordinate system 
    output_raster.GetRasterBand(1).WriteArray(vals_timestep_adjusted)   
    print 'exported raster # : ' + str(index)   
    return fileName
    
   
def update_collection(fileName, col, name, CRS, timeInterval, timeOrigin, threed='top'):
    p = subprocess.Popen("rasimport -f %s --coll %s --coverage-name %s --crs-uri '%%SECORE_URL%%/crs/EPSG/0/%s':'%%SECORE_URL%%/crs/OGC/0/AnsiDate' --crs-order 1:0:2 --3D %s --csz %s --shift 0:0:%s" % (str(fileName), str(col), str(name), str(CRS), str(threed), str(timeInterval), str(timeOrigin)), stderr=subprocess.STDOUT, shell=True, stdout=subprocess.PIPE)
    p.wait()
    output = p.stdout.read()
    if len(output) == 0:
        print 'raster imported to the database'
    else:
        print output
    p.stdout.close()

if __name__ == '__main__':

    # Change those below
    filePath = '/home/rasdaman/evaporation.nc'
    workspace = '/home/rasdaman/rasters'
    key = 'tp'
    col = 'testdata'
    name = 'testraster'
    CRS = 4326
    ncFile, lon, lat, time_list = readNetCDF(filePath)
    # and this:
    time_list = time_list[:1000]
    
    for index, timestep in enumerate(time_list):
        timeInterval = 1
        timeOrigin = time_list[0] if index == 0 else 0
        
        fileName = writeTiff(ncFile, lon, lat, index, key, workspace)
#    update_collection(fileName, col, name, CRS, timeInterval, timeOrigin)


