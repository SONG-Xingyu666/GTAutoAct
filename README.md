# GTAutoAct: An Automatic Datasets Generation Framework Based on Game Engine Redevelopment for Action Recognition
![overall](/resources/overall.png)
GTAutoAct is a innovative dataset generation framework leveraging game engine technology to facilitate advancements in action recognition. 
GTAutoAct excels in automatically creating large-scale, well-annotated datasets with extensive action classes and superior video quality. 

## Project Setup

### FiveM Server
To setup GTAutoAct, you need a Rockstar account and setup a FiveM server.
For tutorial please refer to [FiveM offical website](https://fivem.net/)

### 3ds MAX
To view your animations, you will need a 3D modeling tool. We recommend 3ds Max. You can setup by [the offical website](https://www.autodesk.com/).

### AnimKit
To make a dictionary for your costomized animation, please download Animkit from [their website](https://forum.cfx.re/t/announcing-animkit-create-your-own-custom-animations-for-fivem/4778132).

### CodeWalker
To edit your map for presenting your animation, please download CodeWalker through [their website](https://www.gta5-mods.com/tools/codewalker-gtav-interactive-3d-map).

### OpenIV
To mangage your animation library, please download OpenIV from [this website](https://openiv.com/).

## 3D Pose Estimation
First, you need to obatin the human skeleton keypoint coordinates by 3D pose estimation. To adress this, we recommend [HRNet](https://openaccess.thecvf.com/content_CVPR_2019/html/Sun_Deep_High-Resolution_Representation_Learning_for_Human_Pose_Estimation_CVPR_2019_paper.html) for 2D wholebody pose extimatiom, and [JointFormer](https://github.com/seblutz/JointFormer) for 2D-to-3D pose lifting. Also, we provide the inferencers for these two models, which can be found in `/inferencer`. Additionally, we recommend to use ["COCO-Wholebody"](https://github.com/jin-s13/COCO-WholeBody) for the 2D pose extimation training, and ["H3WB"](https://github.com/wholebody3d/wholebody3d) for the 3D lifting. GTAutoAct supports both COCO-Wholebldy and NTU-RGB+D layouts.

## Action Animation
For Action Animation, please refer to ["animation_generation"](project_code/animation_generation/README.md) section.

## Auto-collection
For Auto-collection, please refer to ["dataset_generation"](project_code/dataset_generation/README.md) section.

## Evaluation
For evaluation, please refer to ["ecaluation_code"](evaluation_code/README.md) section.















