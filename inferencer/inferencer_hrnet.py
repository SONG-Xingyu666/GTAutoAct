from mmpose.apis.inferencers import MMPoseInferencer, get_model_aliases

def inference(input_path, pose_2d_config_path, pose_2d_ckpt_path, output_path):
    inferencer = MMPoseInferencer(
        pose2d=pose_2d_config_path,
        pose2d_weights=pose_2d_ckpt_path)
    res_generator = inferencer(inputs=input_path, show=False, out_dir=output_path)
    res = next(res_generator)
    
if __name__ == '__main__':
    input_path = r''
    output_path = r'vis_results'
    pose_2d_config_path = r''
    pose_2d_ckpt_path = r''
    inference(input_path=input_path, pose_2d_config_path=pose_2d_config_path, pose_2d_ckpt_path=pose_2d_ckpt_path, output_path=output_path)