# Animation Generation

Generating animation list automatically. 

Input: skeleton coordinate list.

Output: animation file.

## Utilization

`"input_folder_path"`: path to your input folder.

`"output_foler_path"`: path to your output folder.

`"frame"`: the index of frame to be animated, default as "None", stands for all the frames within an action. 

`"animation_movement"`: flag of presenting position movement during the presentation. Default as "False".

`"frame_rate"`: frame rate of the animation.

`"interplation_interval"`: the interval of frame interplation, default as 1 (without interplation).

`"SequenceFrameLimit"`: limitation of sequence of quaternion within a frame.

`"smooth"`: flag of frame smoothing operation.

Run `main.py`.










