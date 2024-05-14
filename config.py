
import os
Stable_diff_api="http://192.168.101.13:7861"

# 此处可以添加额外的配置
Stable_diff_conf={
    # 支持payload中的参数直接写入,会改变生成图片的效果如:
    #   "enable_hr": false,
    #   "denoising_strength": 0,
    #   "firstphase_width": 0,
}

# 配置ImageMagick的路径
x= r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"



# 此处用于给生成每张图片的时候都添加的修饰关键字,比如"4K 高清 柔和......"
# 例子:
# ADDER_PROMOTE="柔和, 古风"

ADDER_PROMOTE=""



# 数组从1开始
# payload = {
#   "enable_hr": false,
#   "denoising_strength": 0,
#   "firstphase_width": 0,
#   "firstphase_height": 0,
#   "hr_scale": 2,
#   "hr_upscaler": "string",
#   "hr_second_pass_steps": 0,
#   "hr_resize_x": 0,
#   "hr_resize_y": 0,
#   "prompt": "",     #  提示词
#   "styles": [
#     "string"
#   ],
#   "seed": -1,
#   "subseed": -1,
#   "subseed_strength": 0,
#   "seed_resize_from_h": -1,
#   "seed_resize_from_w": -1,
#   "sampler_name": "string",
#   "batch_size": 1,
#   "n_iter": 1,
#   "steps": 50,
#   "cfg_scale": 7,
#   "width": 512,
#   "height": 512,
#   "restore_faces": false,
#   "tiling": false,
#   "do_not_save_samples": false,
#   "do_not_save_grid": false,
#   "negative_prompt": "string",     #  负面提示词
#   "eta": 0,
#   "s_churn": 0,
#   "s_tmax": 0,
#   "s_tmin": 0,
#   "s_noise": 1,
#   "override_settings": {},
#   "override_settings_restore_afterwards": true,
#   "script_args": [],
#   "sampler_index": "Euler",
#   "script_name": "string",
#   "send_images": true,
#   "save_images": false,
#   "alwayson_scripts": {}
# }
