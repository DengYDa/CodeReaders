from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseProcessor(ABC):
    """处理器基类"""
    @abstractmethod
    def process(self, input_data: Any) -> List[Dict]:
        pass