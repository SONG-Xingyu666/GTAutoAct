# GTAutoAct: An Automatic Datasets Generation Framework Based on Game Engine Redevelopment for Action Recognition
![overall](https://github.com/SONG-Xingyu666/cvpr24_GTAutoAct/blob/main/resources/overall.pdf)

Current datasets for action recognition tasks face limitations stemming from traditional collection and generation methods, including the constrained range of action classes, absence of multi-viewpoint recordings, limited diversity, poor video quality, and labor-intensive manually collection. 
To address these challenges, we introduce GTAutoAct, a innovative dataset generation framework leveraging game engine technology to facilitate advancements in action recognition. 
GTAutoAct excels in automatically creating large-scale, well-annotated datasets with extensive action classes and superior video quality. 
Our framework's distinctive contributions encompass: 
(1) it innovatively transforms readily available coordinate-based 3D human motion into rotation-orientated representation with enhanced suitability in multiple viewpoints; 
(2) it employs dynamic segmentation and interpolation of rotation sequences to create smooth and realistic animations of action; 
(3) it offers extensively customizable animation scenes; 
(4) it implements an autonomous video capture and processing pipeline, featuring a randomly navigating camera, with auto-trimming and labeling functionalities. 
Experimental results underscore the framework's robustness and highlights its potential to significantly improve action recognition model training.


## Experiment Setup
We suggest utilizing MMAction, an open-source toolbox designed for video understanding, which is based on the PyTorch framework.
For setting up MMAction, please follow the setup instructions available on its ["official GitHub repository"](https://github.com/open-mmlab/mmaction2). 
For reference, the details of our experimental environments are outlined in Section B.1. of the appendix.

## Download Requirements
```
pip install -r requirements.txt
```

## Data Preparation
Regarding the Human3.6M dataset, please refer to ["H36M"](http://vision.imar.ro/human3.6m/description.php).
Regarding the NTU RGB+D dataset, please refer to ["NTU RGB+D"](https://rose1.ntu.edu.sg/dataset/actionRecognition/).
Regarding the H3WB dataset, please refer to ["H3HB"](https://github.com/wholebody3d/wholebody3d).
After downloading each dataset, use *`data_preparation.py`* to prepare the datasets.
```
python data_preparation.py ${input_path} ${output_path}
```
After generating datasets, make sure the dataset is named as "Kinectics400", and placed in the following path: 
```
Path2MMAction/mmaction2/data/
```

## Model Configuration
For detailed information on the configuration of each model used in our experiments, please refer to Section B.2. of the appendix. 
This section contains specific implementation details crucial for replicating or understanding our models' setups.
Alternatively, you can directly download the configuration file for each model from our ["project repository"](https://anonymous.4open.science/r/GTAutoAct-4CB6/README.md). 
Additionally, we have included several configuration files in the following path:
```
testing_code/config/
```
Please place config files under your main MMAction project.

## Checkpoint
To facilitate easy reproduction of our results, we have provided the trained checkpoints for each model corresponding to each dataset on our ["project repository"](https://anonymous.4open.science/r/GTAutoAct-4CB6/README.md). 
Please place ckpt files under your main MMAction project. 
This allows for straightforward replication and analysis of our experimental findings.

## Evaluation
For evaluation purposes, you can either follow the official instruction file of MMAction or download our custom testing code, designed for batch processing on server or supercomputer systems. 
Additionally, we have included run files in the following path:
```
testing_code/run_file
``` 
This code is also available in our repository and is tailored for efficient, large-scale evaluation of the models. 
You can run the test on server by:
```
sh test_server.sh
```
Or run the test on supercomputer by:
```
sh test_sc.sh
```












