# Pollinator monitoring in flower-enriched maize using an iterative AI-assisted annotation pipeline and visual surveys

This is the official code repo for our paper entitled "Pollinator monitoring in flower-enriched maize using an iterative AI-assisted annotation pipeline and visual surveys" which is currently under review.

# Reproducing Paper's Results
## Datasets
Download our [validation data](https://www.ipb.uni-bonn.de/html/projects/bee_detection_chong2024aeee/dataset/final_dataset/bee_chong_seidel_validation_set.zip) as a sample of our dataset.
We will make our full dataset public upon the paper's acceptance. Till then, email me (Linn) for early access to our data.
If you are from IPB, the data is on our dataserver 😉
<!--You can download our dataset at [phenoroam](https://phenoroam.phenorob.de/geonetwork/srv/eng/catalog.search#/metadata/1d1e8330-c6bb-486d-8636-16355ef72e99). -->

For reproducibility, we also provide the annotations from each iteration (this is needed to reproduce our graphs)
+ [iteration 0 annotations](https://www.ipb.uni-bonn.de/html/projects/bee_detection_chong2024aeee/dataset/)
+ [iteration 1 annotations](https://www.ipb.uni-bonn.de/html/projects/bee_detection_chong2024aeee/dataset/)
+ [iteration 2 annotations](https://www.ipb.uni-bonn.de/html/projects/bee_detection_chong2024aeee/dataset/)
+ [iteration 3 annotations](https://www.ipb.uni-bonn.de/html/projects/bee_detection_chong2024aeee/dataset/)
+ [iteration 4 annotations](https://www.ipb.uni-bonn.de/html/projects/bee_detection_chong2024aeee/dataset/)
+ [iteration 5 annotations](https://www.ipb.uni-bonn.de/html/projects/bee_detection_chong2024aeee/dataset/)
+ [manual quality control annotations](https://www.ipb.uni-bonn.de/html/projects/bee_detection_chong2024aeee/dataset/)


## Weights 

To fully reproduce the results of YOLOv5 used in our iterative computer vision pipeline, you will also need to download the model weights:
+ [iteration 1 checkpoint](https://www.ipb.uni-bonn.de/html/projects/bee_detection_chong2024aeee/checkpoints/)
+ [iteration 2 checkpoint](https://www.ipb.uni-bonn.de/html/projects/bee_detection_chong2024aeee/checkpoints/)
+ [iteration 3 checkpoint](https://www.ipb.uni-bonn.de/html/projects/bee_detection_chong2024aeee/checkpoints/)
+ [iteration 4 checkpoint](https://www.ipb.uni-bonn.de/html/projects/bee_detection_chong2024aeee/checkpoints/)
+ [iteration 5 checkpoint](https://www.ipb.uni-bonn.de/html/projects/bee_detection_chong2024aeee/checkpoints/)

We also have the [weights for YOLOv5 trained on the final dataset](https://www.ipb.uni-bonn.de/html/projects/bee_detection_chong2024aeee/checkpoints/).


# Installation
## Requirements
Our code was tested on a Linux machine, with Python 3.7.13.

## Environment setup
Use pip to setup your favourite virtual environment (venv/conda/etc)
```bash
git clone --recurse-submodules https://github.com/yuelinn/bee_detection.git
cd bee_detection
pip install -r requirements.txt
```
You may need to install PyTorch separately if you have specific version requirements.


# Usage
## Training YOLOv5 for AI-assisted labelling
1. Download the images to ${PARENT_DIR}/images
2. Download the annotations to ${PARENT_DIR}/annotations/iteration_0
3. Generate the patches
```bash
```
4. You may want to visualise the patches as a sanity check (see how to section on visualise)
5. Train using the patches
```bash
```

## Training YOLOv5 on the full dataset
```bash
```

## Evaluating YOLOv5
```bash
```

## Generating labels for manual annotation
```bash
```


## Generating plots from the annotations
```python
python 
```

# Visualisation
You can visualise the bounding boxes from the annotations or the predictions
using my repo yolo-labels-python-visualiser.
```bash
cd yolo-labels-python-visualiser

```
# Citation
If you use this code for academic purposes, cite the paper:
TBD

# Prior work

For our previous work for the module NPW301, please refer to the branch `npw301`.



