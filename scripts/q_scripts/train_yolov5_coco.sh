
#block(name=[yolov5-train-coco], threads=6, memory=32000, subtasks=1, gpus=1, hours=240)

source ~/.bashrc;
conda activate yolov5_bee;
python --version
cd /home/beestudents/Linn_Julian_phenotyping/yolov5;
python train.py --data coco.yaml --cfg yolov5m.yaml --weights '' --batch-size 24 --workers 3;


