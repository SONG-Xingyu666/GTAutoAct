# Evaluation for GTAutoAct
The complete project code for GTAutoAct is accessible via an anonymous link for a private GitHub repository, which can be found here:["Project code repository"](https://anonymous.4open.science/r/GTAutoAct-4CB6/README.md).
Due to the license agreements concerning the use of the Human3.6M, NTU RGB+D, and H3WB datasets, we are unable to distribute any datasets derived from these sources. 
This restriction includes all H36M-based datasets such as H36M-Original, H36M-Single, H36M-Extracted, H36M-SingleExtracted, H36M-Original-Test, and H36M-Segment-Test, as well as any NTU-based datasets, including NTU-Original and NTU-Test.
However, we offer the scripts needed to generate these datasets from the original sources, and these can be accessed and downloaded from the Project code repository as well.
Additionally, the datasets generated by GTAutoAct are available for download through an anonymous link to a private Google Drive. The link can be found here: ["Datasets"](https://drive.google.com/drive/folders/1rZm-IZT45KjDLVDC3C_qOn7IPGVokPKH?usp=drive_link).

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
