conda activate openmmlab

cd mmaction2/

python tools/test.py Path2Configs/config.py Path2Ckpts/ckpt.pth 8 --work-dir work_dir/
