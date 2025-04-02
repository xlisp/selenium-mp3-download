import os
import re

def remove_chinese_numbered_files(directory='.'):
    # Regular expression pattern to match Chinese characters and numbers in parentheses
    pattern = re.compile(r'.*[\u4e00-\u9fff]+.*\(\d+\)\..*')
    
    removed_files = []
    for filename in os.listdir(directory):
        if pattern.match(filename):
            try:
                file_path = os.path.join(directory, filename)
                os.remove(file_path)
                removed_files.append(filename)
                print(f"Removed: {filename}")
            except OSError as e:
                print(f"Error removing {filename}: {e}")
    
    if not removed_files:
        print("No matching files found to remove.")
    else:
        print(f"\nTotal files removed: {len(removed_files)}")

if __name__ == "__main__":
    # You can specify a directory path as an argument, or it will use the current directory
    remove_chinese_numbered_files()

