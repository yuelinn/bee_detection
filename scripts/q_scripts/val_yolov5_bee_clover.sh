
#block(name=[yolov5-val-clover], threads=2, memory=32000, subtasks=1, gpus=1, hours=240)

source ~/.bashrc;
conda activate yolov5_bee;
python --version
cd /home/beestudents/Linn_Julian_phenotyping/yolov5;
python val.py --data bee_clover.yaml --weights '/home/beestudents/Linn_Julian_phenotyping/yolov5/runs/train/exp18/weights/best.pt' --batch-size 2 --img 1280 --name clover-test-final; 


