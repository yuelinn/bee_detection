# Image-based Bee Detection in the Field using Machine Learning

Given the important role bees play in our ecosystem,
we would like to be able to quantitatively measure the activity of bees in their natural environment. 

Thus, our work presented here proposes a method to collect data, label data, and apply a machine learning method to detect honey bees and bumblebees.
Using the results from the machine learning method, we also showed some example analysis which can be performed. 

Specifically, we collected over 5549 images using a static camera, in nadir position over three different types of plants. From the images we collected, we labelled 2670 images by manually with bounding boxes, for 2 types of bees (honey bee vs bumble bee).
Refer to [this section on the dataset developed](https://github.com/yuelinn/bee_detection/wiki/Dataset) for more information.

We used the data we labelled to train the Neural Network, [YOLOv5](https://github.com/yuelinn/yolov5) to detect honey bees and bumblebees.
Below is the precision-recall curve for the phacelia-rapeseed plants. We achieved a mean Average Precision (mAP) of 0.509 at IoU of 0.5.
Refer to [this section on the machine learning method](https://github.com/yuelinn/bee_detection/wiki/Machine-Learning) for more information.

Using the detections from the machine learning method, YOLOv5, we can perform some analysis of the bees present in the data collected. We propose using "heat maps" to indicate the frequency a location bees were detected in a given image sequence. With the heat map, we can analyse where the bees tend to prefer to go, which may indicate the bees' preference to specific plants.
Refer to [this section on the analysis using heat maps](https://github.com/yuelinn/bee_detection/wiki/Heat-maps) for more information.

The work presented here was done by Linn Chong and Julian Bauer, under the supervision of Jana Kierdorf, Lukas Drees, and Prof. Dr.-Ing. Ribana Roscher at the University of Bonn for the module NPW 031.
