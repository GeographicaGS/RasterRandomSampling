# Raster Random Sampling
Sampling raster data with a fast (Numpy) random coordinates generator. Output is a Shapefile.

Performance:
[IPython notebook]](https://github.com/GeographicaGS/RasterRandomSampling/blob/master/raster_random_sampling.ipynb)

## Main features
- Using Numpy to generate random coordinates.
- You can seed the generator.
- Using Fiona + Shapely to handle vector data.
- Two flavors to sample raster data: Rasterio and GDAL (gdallocationinfo). Rasterio is ultrafast (it is the best choice for big samples).

## Requirements
- Numpy
- Fiona
- Shapely
- Rasterio
- Pyprind
- GDAL

## Usage
Random coordinates generation with raster sampling (using Rasterio = ultrafast sampling):
```python
from rasterrandomsampling import RasterRandSampl

def runTest():
rcg = RasterRandSampl()

bbox = (90., 180., -90., -180.)

res = rcg.randLatLon(bbox, 1000, 10)

rst_smp = ("data/raster_test.tif", "rasterio")

outputfile = "/tmp/out_rnd_rasterio.shp"

rcg.createShp(outputfile, res, raster_sampling=rst_smp)

if __name__ == '__main__':
    runTest()
```

Random coordinates generation with raster sampling (using gdal = slow for big samples):
```python
from rasterrandomsampling import RasterRandSampl

def runTest():
    rcg = RasterRandSampl()

    bbox = (90., 180., -90., -180.)

    res = rcg.randLatLon(bbox, 1000, 10)

    rst_smp = ("data/raster_test.tif", "gdal")

    outputfile = "/tmp/out_rnd_gdal.shp"

    rcg.createShp(outputfile, res, raster_sampling=rst_smp)

if __name__ == '__main__':
    runTest()
```

Random coordinates generation without raster sampling:
```python
from rasterrandomsampling import RasterRandSampl

def runTest():
    rcg = RasterRandSampl()

    bbox = (90., 180., -90., -180.)

    res = rcg.randLatLon(bbox, 1000, 10, seed=1)

    outputfile = "/tmp/out_rnd.shp"

    rcg.createShp(outputfile, res, raster_sampling=None)

if __name__ == '__main__':
    runTest()
```

Random coordinates generation without raster sampling (seeding generator):
```python
from rasterrandomsampling import RasterRandSampl

def runTest():
    rcg = RasterRandSampl()

    bbox = (90., 180., -90., -180.)

    res = rcg.randLatLon(bbox, 1000, 10)

    outputfile = "/tmp/out_rnd.shp"

    rcg.createShp(outputfile, res, raster_sampling=None)

if __name__ == '__main__':
    runTest()
```
