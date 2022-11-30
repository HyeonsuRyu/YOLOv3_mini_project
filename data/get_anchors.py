import json
import os
import math
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns; sns.set()

"""
the original train.json file format:
[
    {
        "name": "image_name",
        "labels": [
            {
                "id": "label_id",
                "category": "label_category",
                "attributes": {
                    "crowd": false,
                    "occluded": false,
                    "truncated": false,
                }
                "box2d": {
                    "x1": 0.0,
                    "x2": 0.0,
                    "y1": 0.0,
                    "y2": 0.0,
                }
            }
            . . .
        ]
    }
]
"""

train_path = "/dataset/train.json"

with open(train_path, "r") as ftr:
    trlabel = json.load(ftr)

# label dict
# not implemented

# get all boxes
w, h = list(), list()
for ind1 in range(len(trlabel)):
    for ind2 in range(len(trlabel[ind1]["labels"])):
        try:
            a = trlabel[ind1]["labels"][ind2]["box2d"]
            x1, y1, x2, y2 = tuple(a.values())
            width = abs(x2 - x1); height = abs(y2 - y1)
            w.append(width); h.append(height)
        except:
            pass

# reshape
x = [w, h]
x = np.asarrray(x)
x = x.transpose()

# set anchor number
n_anchor = 9

# K-means
from sklearn.cluster import KMeans
kmeans3 = KMeans(n_clusters = n_anchor)
kmeans3.fit(x)
y_kmeans3 = kmeans3.predict(x)

#get the centers of the clusters
centers3 = kmeans3.cluster_centers_

yolo_anchor_average = list()
for ind in range(n_anchor):
    yolo_anchor_average.append(np.mean(x[y_kmeans3==ind], axis=0))

yolo_anchor_average = np.array(yolo_anchor_average)

# set resolution
resolution_x = 1280
resolution_y = 720
target_resolution = 608

# show the result
plt.scatter(x[:, 0], x[:, 1], c=y_kmeans3, s=2, cmap='viridis')
plt.scattter(yolo_anchor_average[:, 0], yolo_anchor_average[:, 1], c='red', s=50)
anchors = yolo_anchor_average
anchors[:, 0] = yolo_anchor_average[:, 0] / resolution_x * target_resolution
anchors[:, 1] = yolo_anchor_average[:, 1] / resolution_y * target_resolution
anchors = np.rint(anchors)
fig, ax = plt.subplots()
for ind in range(n_anchor):
    rectangle = plt.Rectangle((target_resolution/2-anchors[ind, 0]/2, target_resolution/2-anchors[ind, 1]/2), anchors[ind, 0], anchors[ind, 1], fc='b', edgecolor='b', fill=None)
    ax.add_patch(rectangle)
ax.set_aspect(1.0)
plt.axis([0, target_resolution, 0, target_resolution])
plt.show()

anchors.sort(axis=0)
print("Your anchor boxes are {}".format(anchors))
# save the result
F = open("/anchors.txt", "w")
F.write("{}".format(anchors))
F.close()