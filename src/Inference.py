import os
import numpy as np
from osgeo import gdal
import caffe
import matplotlib.pyplot as plt

root_dir = "/home/guillaume/Documents/SegNet"
model_def = os.path.join(root_dir, "resources/deconvnet_deploy.prototxt")
model_weights = os.path.join(root_dir, "resources/deconvnet_iter_100.caffemodel")

net = caffe.Net(model_def, caffe.TEST, weights=model_weights)
data_path = "/home/guillaume/Documents/SegNet/data/Data_224x224/Data/RGB_PAN_Paris_00001_224_224.tif"
label_path = "/home/guillaume/Documents/SegNet/data/Data_224x224/Labels/CLASS_SEG_Paris_00001_224_224.tif"
# data_path = "/home/guillaume/Documents/SegNet/data/Data_224x224/Data/RGB_PAN_Paris_00524_224_224.tif"
# label_path = "/home/guillaume/Documents/SegNet/data/Data_224x224/Labels/CLASS_SEG_Paris_00524_224_224.tif"
data = np.array(gdal.Open(data_path).ReadAsArray())
label = np.array(gdal.Open(label_path).ReadAsArray())

print data.shape, data.dtype
print label.shape, label.dtype

out = net.forward_all(data=np.expand_dims(data, axis=0))
logits = out["logits"]

print logits.shape, logits.dtype

img = np.transpose(data, axes=[1, 2, 0])
# prediction = 1. / (1. + np.exp(-logits[0, 0]))
prediction = logits[0, 0]
plt.figure()
plt.subplot(1, 3, 1)
plt.imshow(img)
plt.subplot(1, 3, 2)
plt.imshow(label)
plt.subplot(1, 3, 3)
plt.imshow(prediction)
plt.show()