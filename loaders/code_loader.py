from typing import List
import os
from .base import BaseLoader
from ..utils.file_utils import get_file_content, is_valid_file

class CodeLoader(BaseLoader):
    """代码文件加载器"""
    def __init__(self, file_extensions: List[str]):
        self.file_extensions = file_extensions
        
    def load(self, project_path: str) -> List[str]:
        code_files = []
        for root, _, files in os.walk(project_path):
            for file in files:
                if is_valid_file(file, self.file_extensions):
                    code_files.append(os.path.join(root, file))
        return code_files