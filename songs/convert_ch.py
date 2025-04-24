import opencc

def convert_traditional_to_simplified(input_file, output_file):
    # 创建繁体到简体的转换器
    converter = opencc.OpenCC('t2s')
    
    try:
        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 转换内容
        simplified_content = converter.convert(content)
        
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(simplified_content)
            
        print(f"转换成功！结果已保存到 {output_file}")
        
    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_file}")
    except Exception as e:
        print(f"错误：{str(e)}")

if __name__ == "__main__":
    input_file = "lll.txt"
    output_file = "lll_simplified.txt"
    convert_traditional_to_simplified(input_file, output_file)

