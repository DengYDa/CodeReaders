# core/base.py
from abc import ABC, abstractmethod
from typing import Any, List, Dict

class BaseComponent(ABC):
    """所有组件的基类"""
    @abstractmethod
    def initialize(self, **kwargs):
        pass