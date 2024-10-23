import matplotlib.pyplot as plt
import os
import json
import numpy as np

def plot_hist(V1, V2, V3, save_path, X1, X2, X3, Y1, Y2, Y3):
    plt.figure(figsize=(12, 6), dpi=100)  

    plt.subplot(1, 3, 1)  
    plt.hist(V1.clone().view(-1).detach().cpu().numpy(), bins=100, color='blue', alpha=0.7)  
    plt.xlabel(X1)
    plt.ylabel(Y1)

    plt.subplot(1, 3, 2) 
    plt.hist(V2.clone().view(-1).detach().cpu().numpy(), bins=100, color='blue', alpha=0.7)  
    plt.xlabel(X2)
    plt.ylabel(Y2)


    plt.subplot(1, 3, 3) 
    plt.hist(V3.clone().view(-1).detach().cpu().numpy(), bins=100, color='blue', alpha=0.7)  
    plt.xlabel(X3)
    plt.ylabel(Y3)

    plt.tight_layout()  
    plt.savefig(save_path)  # 保存为PNG文件 

def plot_hist_quantization(Q_feat, Q_scaling, Q_offsets, save_path=''):
    '''
    Plot the distributions of Q
    '''
    plot_hist(Q_feat, Q_scaling, Q_offsets, save_path, 'Q_feat Value', 'Q_scaling Value', 'Q_offsets Value', 'Counts', 'Counts', 'Counts')

def plot_hist_mean(mean_feat, mean_scaling, mean_offsets, save_path=''):
    '''
    Plot the distributions of mean
    '''
    plot_hist(mean_feat, mean_scaling, mean_offsets, save_path, 'mean_feat Value', 'mean_scaling Value', 'mean_offsets Value', 'Counts', 'Counts', 'Counts')

def plot_hist_scale(scale_feat, scale_scaling, scale_offsets, save_path=''):
    '''
    Plot the distributions of scale
    '''
    plot_hist(scale_feat, scale_scaling, scale_offsets, save_path, 'scale_feat Value', 'scale_scaling Value', 'scale_offsets Value', 'Counts', 'Counts', 'Counts')


def plot_RD_curve(metric='psnr', save_path='', notation=False, filter:list=None):  
    '''
        Plot R-D Curve in one experiment

        metric: ['psnr', 'ssim', 'lpips', 'fps']

        save_path: path to save the curve

        notation: True/False, whether to notate the lambda in corresponding points

        filter: list of str that will be excluded in plotting
    '''
    plt.figure(figsize=[15, 12], dpi=100)  
    
    # 存储所有的 x 和 y 数据以便后续设置坐标轴范围  
    all_x = []  
    all_y = []  
    
    # 获取文件列表  
    json_files = [file for file in os.listdir(save_path) if file.endswith('.json')]  
    num_files = len(json_files)  
    
    # 生成颜色映射  
    colors = plt.cm.nipy_spectral(np.linspace(0, 1, num_files))  
    # print(dir(plt.cm))
    # colors = plt.cm.viridis(np.random.uniform(0, 1, num_files))  
    
    for idx, file in enumerate(json_files): 
        continue_flag = True
        if filter:
            for ft in filter:
                if ft in file:
                    continue_flag = False
        if continue_flag and filter is not None:
            continue

        with open(os.path.join(save_path, file), 'r') as f:  
            data = json.load(f)  
        file_name = os.path.splitext(file)[0]  
        l_list = list(data.keys())  
        x_list = [float(data[l]['total_size']) for l in l_list]  
        y_list = [round(float(data[l][metric]), 4) for l in l_list]  
        
        # 添加到所有数据列表中  
        all_x.extend(x_list)  
        all_y.extend(y_list)  
        
        plt.plot(x_list, y_list, '-o', label=file_name, color=colors[idx])  

        if notation:
            for i in range(len(l_list)):  
                plt.annotate(f'{l_list[i]}', (x_list[i], y_list[i]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=5, color='blue')  

    # 设置坐标轴范围  
    plt.xlim(min(all_x)-0.5, max(all_x)+0.5)  
    plt.ylim(min(all_y)-0.5, max(all_y)+0.5)  

    plt.legend()  
    plt.xlabel('Size/MB')  
    plt.ylabel(metric.upper())  
    plt.grid()  
    plt.title('R-D Curve in ' + os.path.basename(save_path))  
    plt.savefig(os.path.join(save_path, 'RD_Curve.png'))  
    plt.close()  
