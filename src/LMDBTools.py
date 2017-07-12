import os
import lmdb
import numpy as np
from osgeo import gdal
from caffe.proto import caffe_pb2
from caffe.io import datum_to_array, array_to_datum

gdal.UseExceptions()


def write_in_lmdb(tile_dir, heatmap_dir, db_dir, step=1000):
    tile_names = sorted(os.listdir(tile_dir))
    heatmap_names = sorted(os.listdir(heatmap_dir))
    with lmdb.Environment(db_dir) as env:
        for i in range(0, len(tile_names), step):
            with lmdb.Transaction(env, write=True, buffers=True) as txn:
                for tile_name, heatmap_name in zip(tile_names[i:i + step], heatmap_names[i:i + step]):
                    print tile_name, heatmap_name
                    tile_path = os.path.join(tile_dir, tile_name)
                    tile_ds = gdal.Open(tile_path)
                    tile = np.array(tile_ds.ReadAsArray())
                    tile = tile[:-1, ...]
                    print tile.shape

                    heatmap_path = os.path.join(heatmap_dir, heatmap_name)
                    heatmap_ds = gdal.Open(heatmap_path)
                    heatmap = np.array(heatmap_ds.ReadAsArray())
                    heatmap = heatmap.reshape([1] + list(heatmap.shape))
                    print heatmap.shape

                    datum = array_to_datum(tile, heatmap)
                    key = tile_name.replace("Tile_", "").replace(".tif", "")
                    print key
                    txn.put(key.encode("ASCII"), datum.SerializeToString())


root_dir = "/home/guillaume/Documents/SegNet/data/Oakland_224x224"
tile_dir = os.path.join(root_dir, "Tiles")
heatmap_dir = os.path.join(root_dir, "Heatmaps")
db_dir = os.path.join(root_dir, "OaklandLMDB")
write_in_lmdb(tile_dir, heatmap_dir, db_dir)
