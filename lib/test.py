# -*- coding: utf-8 -*-
#
#  Author: Cayetano Benavent, 2015.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

from rasterrandomsampling import RasterRandSampl


def runTest():
    rcg = RasterRandSampl()

    # bbox = (90., 180., -90., -180.)
    # bbox = (20., 20., -20., -20.)
    bbox = (42., 10., 32., -10.)

    # res = rcg.randLatLon(bbox, 10, 1)
    # res = rcg.randLatLon(bbox, 10, 2)
    # res = rcg.randLatLon(bbox, 10, 0.5)
    # res = rcg.randLatLon(bbox, 10, 4)
    res = rcg.randLatLon(bbox, 100, 10)
    # res = rcg.randLatLon(bbox, 1000, 10, seed=1)

    # rcg.createShp("/tmp/out_rnd.shp", res, raster_sampling=None)
    # rcg.createShp("/tmp/out_rnd_gdal.shp", res, raster_sampling=("data/raster_test.tif", "gdal"))
    rcg.createShp("/tmp/out_rnd_rasterio.shp", res, raster_sampling=("data/raster_test.tif", "rasterio"))

if __name__ == '__main__':
    runTest()
