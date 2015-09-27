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

import numpy as np
import pyprind
import logging
import subprocess
import rasterio
from shapely.geometry import Point, mapping
from fiona import collection
from fiona.crs import from_epsg



class RasterRandSampl(object):

    def __init__(self, loglevel="INFO"):

        self.logger = self.__loggerInit(loglevel)


    def __loggerInit(self, loglevel):
        """
        Logger init...
        """
        if loglevel=="INFO":
            __log_level=logging.INFO
        elif loglevel=="DEBUG":
            __log_level=logging.DEBUG
        elif loglevel=="ERROR":
            __log_level=logging.ERROR
        else:
            __log_level=logging.NOTSET

        logfmt = "[%(asctime)s - %(levelname)s] - %(message)s"
        dtfmt = "%Y-%m-%d %I:%M:%S"

        logging.basicConfig(level=__log_level, format=logfmt, datefmt=dtfmt)

        return logging.getLogger()


    def randLatLon(self, bbox, sz, prec, seed=None, paired=True):
        """
        Latitude/Longitude random generator
        -----------------------------------
        bbox : tuple
            (Maximum latitude, Maximum Longitude, lat_min, lon_min)
        sz : int
            sample size
        prec : float
            coordinates precission
              examples
                precission=0.5   2 degree Lat/Lon
                precission=1     1 degree Lat/Lon
                precission=2     0.5 degree Lat/Lon
                precission=4     0.25 degree Lat/Lon
        seed: int, optional (default=None)
            You can seed the generator.
        paired: bool, optional (default=True)
            If True the function returns coordinates paired.

        Returns
        -------
        rnd_coord : ndarray
        """
        try:
            self.logger.info("Generating random coordinates sample...")

            if seed:
                self.logger.info("Seeding the generator (seed={0})...".format(seed))
                np.random.seed(seed)

            lat_max, lon_max, lat_min, lon_min = bbox

            lat = np.linspace(lat_max, lat_min, (180. * prec) + 1)
            lon = np.linspace(lon_min, lon_max, (360. * prec) + 1)

            rnd_coord = np.array((np.random.choice(lat, sz), np.random.choice(lon, sz)))

            if paired:
                rnd_coord = rnd_coord.T

            self.logger.info("Random coordinates sample successfully generated...")

            return rnd_coord

        except Exception as err:
            self.logger.error("Error generating random coordinates sample: {0}".format(err))


    def createShp(self, outputfile, coords, epsg_cd=4326, raster_sampling=None):
        """
        Exporting random points
        to Shapefile format
        -----------------------
        outputfile : str
        coords : ndarray
        epsg_cd : int, optional (default: 4326)
        raster_sampling: tuple(str, sampling_type), optional (default: None)
                Sampling types:
                    raster_sampling=(rasterfilepath, "gdal")
                    raster_sampling=(rasterfilepath, "rasterio")
        """
        try:
            self.logger.info("Exporting sample to Shapefile...")

            if isinstance(raster_sampling, tuple):
                self.logger.info("Sampling values on rasterfile...")

                rst_outfile, rst_smpl_type = raster_sampling[0], raster_sampling[1]

                if rst_smpl_type == "rasterio":
                    smpl_vals = self.__samplePointOnRasterRasterio(rst_outfile, coords)

            schema = {'geometry': 'Point',
                      'properties': {'cod_id': 'int', 'value': 'float' }
                    }

            shp_crs = from_epsg(epsg_cd)

            bar = pyprind.ProgBar(len(coords))

            with collection(outputfile, "w", driver="ESRI Shapefile",
                schema=schema, crs=shp_crs) as output:

                for idx, coord in enumerate(coords, 1):
                    geom = mapping(Point(coord[1], coord[0]))

                    value = 0
                    if raster_sampling:
                        if rst_smpl_type == "gdal":
                            value = self.__samplePointOnRasterGdal(rst_outfile, coord)

                        elif rst_smpl_type == "rasterio":
                            value = float(smpl_vals[idx - 1])

                    output.write({'properties': {'cod_id': idx, 'value': value},
                                  'geometry': geom
                                })
                    bar.update()

            self.logger.info("Sample successfully exported to Shapefile...")

        except Exception as err:
            self.logger.error("Error generating random coordinates sample: {0}".format(err))


    def __samplePointOnRasterRasterio(self, rasterfile, coords, band=1):
        """
        Sampling values on a given
        raster file from a list of
        point locations (lat/lon).

        Using Rasterio library.
        --------------------------------
        rasterfile: str
        coords: ndarray

        Returns
        -------
        values: ndarray
        """
        try:
            coord_lst = [(c[1], c[0]) for c in coords]

            with rasterio.open(rasterfile) as src:
                smpl_vl = src.sample(coord_lst, indexes=[band])

                values = [vl for vl in smpl_vl]

                return values

        except Exception as err:
            self.logger.error("Error sampling points (Rasterio): {1}".format(coords, err))


    def __samplePointOnRasterGdal(self, rasterfile, coords, band=1):
        """
        Sampling values on a given
        raster file from
        point locations (lat/lon).

        It's a gdallocationinfo wrapper
        --------------------------------
        rasterfile: str
        coords: ndarray

        Returns
        -------
        value: float
        """
        try:
            lat, lon = coords
            out = subprocess.check_output(["gdallocationinfo", rasterfile,
                "-b", str(band), "-wgs84", str(lon), str(lat), "-valonly"])
            value = float(out)

            return value

        except ValueError as err:
            # Raise value error when location is off this file. value=NULL
            self.logger.warning("Sampling point is off the raster file. Coords {0}".format(coords))

        except Exception as err:
            self.logger.error("Error sampling point (gdallocationinfo) at coords {0}: {1}".format(coords, err))
