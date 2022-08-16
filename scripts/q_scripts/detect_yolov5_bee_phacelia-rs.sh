
#block(name=[yolov5-detect-clover], threads=2, memory=32000, subtasks=1, gpus=1, hours=5)

source ~/.bashrc;
conda activate yolov5_bee;
python --version
cd /home/beestudents/Linn_Julian_phenotyping/yolov5;
python detect.py --source '/scratch/beestudents/220526/100_2605_1/*.JPG' --weights '/home/beestudents/Linn_Julian_phenotyping/yolov5/runs/train/exp18/weights/best.pt' --img 1280 --save-txt --save-conf;


