
#block(name=[yolov5-val-pr], threads=2, memory=32000, subtasks=1, gpus=1, hours=240)

source ~/.bashrc;
conda activate yolov5_bee;
python --version
cd /home/beestudents/Linn_Julian_phenotyping/yolov5;
python val.py --data bee_phacelia-rapeseed-test.yaml --weights '/home/beestudents/Linn_Julian_phenotyping/yolov5/runs/train/exp18/weights/best.pt' --batch-size 2 --img 1280 --conf-thres 0.001  --save-txt --name pr-test-final;


