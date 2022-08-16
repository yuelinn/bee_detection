
#block(name=[yolov5-train-bee_eg], threads=2, memory=32000, subtasks=1, gpus=1, hours=240)

source ~/.bashrc;
conda activate yolov5_bee;
python --version
cd /home/beestudents/Linn_Julian_phenotyping/yolov5;
python train.py --data bee_eg.yaml --cfg yolov5m.yaml --weights '/home/beestudents/Linn_Julian_phenotyping/yolov5/pretrained/yolov5m.pt' --batch-size 8 --workers 1 --epochs 1000 --img 1280;


