# Raster Random Sampling
Sampling raster data with a fast (Numpy) random coordinates generator. Output is a Shapefile.

## Main features
- Using Numpy to generate random coordinates.
- You can seed the generator.
- Using Fiona + Shapely to handle vector data.
- Two flavors to sample raster data: Rasterio and GDAL (gdallocationinfo). Rasterio is ultrafast (it is the best choice for big samples).

## Usage

Random coordinates generation with raster sampling (using Rasterio = ultrafast sampling):
```python
from rasterrandomsampling import RasterRandSampl

def runTest():
    rcg = RasterRandSampl()

    bbox = (90., 180., -90., -180.)

    res = rcg.randLatLon(bbox, 1000, 10)

    rcg.createShp("/tmp/out_rnd_rasterio.shp", res, raster_sampling=("data/raster_test.tif", "rasterio"))

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

    rcg.createShp("/tmp/out_rnd_gdal.shp", res, raster_sampling=("data/raster_test.tif", "gdal"))

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

    rcg.createShp("/tmp/out_rnd.shp", res, raster_sampling=None)

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

    rcg.createShp("/tmp/out_rnd.shp", res, raster_sampling=None)

if __name__ == '__main__':
    runTest()
```
