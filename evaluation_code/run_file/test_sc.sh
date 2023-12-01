#!/bin/bash

#------ pjsub option --------#
# Modify here

#------- Program execution -------#
source Path2Source/.bashrc
conda activate openmmlab
cd mmaction2/
bash tools/dist_test.sh Path2Configs/config.py Path2Ckpts/ckpt.pth 8 --work-dir work_dir/