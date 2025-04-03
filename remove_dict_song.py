import glob
import os

def remove_txt_content(input_file):
    # 读取所有.txt文件的内容
    txt_contents = set()
    for txt_file in glob.glob("*.txt"):
        if txt_file != input_file:  # 避免处理输入文件本身（如果它也是.txt）
            with open(txt_file, 'r', encoding='utf-8') as f:
                txt_contents.update(line.strip() for line in f)
    
    # 读取输入文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            input_lines = f.readlines()
    except FileNotFoundError:
        print(f"错误：找不到输入文件 '{input_file}'")
        return
    
    # 过滤掉在.txt文件中出现的行
    filtered_lines = [line.strip() for line in input_lines 
                     if line.strip() not in txt_contents]
    
    # 保存结果到新文件
    output_file = f"filtered_{os.path.basename(input_file)}"
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in filtered_lines:
            f.write(line + '\n')
    
    # 显示结果
    print(f"\n处理完成！")
    print(f"原始行数: {len(input_lines)}")
    print(f"过滤后行数: {len(filtered_lines)}")
    print(f"结果已保存到: {output_file}")
    print("\n过滤后的内容:")
    for line in filtered_lines:
        print(line)

if __name__ == "__main__":
    input_file = input("请输入要处理的文件名: ")
    remove_txt_content(input_file)
