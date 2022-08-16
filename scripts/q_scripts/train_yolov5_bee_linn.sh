#block(name=[yolov5-train-bee_linn], threads=4, memory=32000, subtasks=1, gpus=1, hours=240)

source ~/.bashrc;
conda activate yolov5_bee;
python --version
cd /home/beestudents/Linn_Julian_phenotyping/yolov5;
python train.py --data bee_linn.yaml --cfg yolov5m.yaml --weights '/home/beestudents/Linn_Julian_phenotyping/yolov5/runs/train/soft_uk10/weights/last.pt' --batch-size 8 --workers 2 --epochs 300 --img 1280 --name soft_uk_restart --save-period 20;


