import os
# for quick run-through of the whole process
exp_name = 'TMP'

for lmbda in [0.004]:  # Optionally, you can try: 0.003, 0.002, 0.001, 0.0005
    for cuda, scene in enumerate(['truck']):
        one_cmd = f'CUDA_VISIBLE_DEVICES={3} python train.py -s data/tandt/{scene} --eval --lod 0 --voxel_size 0.01 --update_init_factor 16 --iterations 30_0 --start_stat 5 --update_from 15 --update_interval 1 --update_until 150 --start_quantization_single 30 --change_quantization_single_to_variable 100 -m outputs/tandt/{scene}/{exp_name}-{lmbda} --lmbda {lmbda}'
        os.system(one_cmd)