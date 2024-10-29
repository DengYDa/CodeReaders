from typing import List

def get_file_content(file_path: str) -> str:
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def is_valid_file(filename: str, extensions: List[str]) -> bool:
    """检查文件是否是支持的类型"""
    return any(filename.endswith(ext) for ext in extensions)