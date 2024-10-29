from abc import ABC, abstractmethod
from typing import List, Any

class BaseLoader(ABC):
    """文件加载器基类"""
    @abstractmethod
    def load(self, path: str) -> List[Any]:
        pass