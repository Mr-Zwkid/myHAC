import os

for lmbda in [0.004]:  # Optionally, you can try: 0.003, 0.002, 0.001, 0.0005
    for cuda, scene in enumerate(['truck']):
        one_cmd = f'CUDA_VISIBLE_DEVICES={3} python train.py -s data/tandt/{scene} --eval --lod 0 --voxel_size 0.01 --update_init_factor 16 --iterations 30_00 -m outputs/tandt/{scene}/{lmbda} --lmbda {lmbda}'
        os.system(one_cmd)