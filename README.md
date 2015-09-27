# Raster Random Sampling
Sampling raster data with a fast (Numpy) random coordinates generator. Output is a Shapefile.

## Main features
- Using Numpy to generate random coordinates.
- You can seed the generator.
- Using Fiona + Shapely to handle vector data.
- Two flavors to sample raster data: Rasterio and GDAL (gdallocationinfo). Rasterio is ultrafast (it is the best choice for big samples).
