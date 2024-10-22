import os
import json
import re 
from utils.plot_utils import plot_RD_curve

def extract_data_from_log(file):
    # 正则表达式模式  
    total_pattern = r"Total ([0-9\.]+)"
    lambda_pattern = r"lambda=([0-9\.]+)"  
    psnr_pattern = r"PSNR ([0-9\.]+)"  
    ssim_pattern = r"ssim ([0-9\.]+)"  
    lpips_pattern = r"lpips ([0-9\.]+)"  
    fps_pattern = r"Test FPS: ([0-9\.]+)"   

    # 存储提取的数据  
    extracted_data = {} 

    # 逐行读取文件    
    previous_line = ''  
    for line in file:  
        if 'Encoded sizes in MB' in line:
            total_size = re.search(total_pattern, line).group(1)

        # 检查是否包含 "test" 字符  
        if "Test FPS" in line and 'Evaluating test' in previous_line:  
            # 合并前一行和当前行  
            combined_line = previous_line + ' ' + line   

            # 提取数据  
            lambda_value = re.search(lambda_pattern, combined_line)  
            psnr_value = re.search(psnr_pattern, combined_line)  
            ssim_value = re.search(ssim_pattern, combined_line)  
            lpips_value = re.search(lpips_pattern, combined_line)  
            fps_value = re.search(fps_pattern, line)  

            # 如果找到匹配项，则存储结果  
            if total_size and lambda_value and psnr_value and ssim_value and lpips_value and fps_value:  
                extracted_values = {  
                    "total_size": total_size,
                    "psnr": psnr_value.group(1),  
                    "ssim": ssim_value.group(1),  
                    "lpips": lpips_value.group(1),  
                    "fps": fps_value.group(1),  
                } 

                extracted_data[lambda_value.group(1)] = extracted_values
        previous_line = line
    return extracted_data

def traverse_and_extract(base_dir):  
    plot_path_set = set()
    for root, dirs, files in os.walk(base_dir):  
        for file in files:  
            if file == 'outputs.log':  
                log_file_path = os.path.join(root, file)  
                with open(log_file_path, 'r') as log_file:  
                    log_content = log_file.readlines()  
                    extracted_data = extract_data_from_log(log_content)  

                    # 构建输出路径  
                    relative_path = os.path.relpath(root, base_dir)  
                    output_dir = os.path.join('explicit_results', relative_path).rsplit('/', 1)[0]
                    file_name = relative_path.split('/')[-1] + '.json'
                    os.makedirs(output_dir, exist_ok=True)  

                    # 保存为 JSON 文件  
                    output_file_path = os.path.join(output_dir, file_name)  
                    with open(output_file_path, 'w') as json_file:  
                        json.dump(extracted_data, json_file, indent=4)  
                    plot_path_set.add(output_dir)
    return list(plot_path_set)
    
                    

if __name__ == "__main__":
    plot_path_list = traverse_and_extract('outputs')
    # print(plot_path_list)
    for save_path in plot_path_list:
        plot_RD_curve('psnr', save_path, False)
        print(save_path)

    print('Completed!')
    
