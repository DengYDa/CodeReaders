# processors/code_splitter.py
from typing import List, Dict, Optional, Any
from tree_sitter import Parser
from tree_sitter import Language, Parser, Tree, Node
from tree_sitter_languages import get_language, get_parser
import os
from .base import BaseProcessor

class PythonCodeElement:
    """Python代码元素的数据类"""
    def __init__(self, 
                 type: str,  # class, function, method, constant, config
                 name: str,
                 code: str,
                 docstring: Optional[str] = None,
                 parent: Optional[str] = None,
                 start_point: tuple = (0, 0),
                 end_point: tuple = (0, 0)):
        self.type = type
        self.name = name
        self.code = code
        self.docstring = docstring
        self.parent = parent
        self.start_point = start_point
        self.end_point = end_point
        
    def to_dict(self) -> Dict:
        return {
            'type': self.type,
            'name': self.name,
            'code': self.code,
            'docstring': self.docstring,
            'parent': self.parent,
            'location': {
                'start': self.start_point,
                'end': self.end_point
            }
        }

class TreeSitterCodeParser:
    """使用tree-sitter解析Python代码"""
    def __init__(self):
        # 初始化tree-sitter
        self.parser = get_parser('python')
        self.PY_LANGUAGE = get_language('python')
        
    def _extract_docstring(self, node: Node, source_code: str) -> Optional[str]:
        """提取节点的文档字符串"""
        for child in node.children:
            if child.type == 'expression_statement':
                string_node = child.children[0]
                if string_node.type in ('string', 'string_literal'):
                    return source_code[string_node.start_byte:string_node.end_byte].strip('"""\'\'\'')
        return None
        
    def _get_node_code(self, node: Node, source_code: str) -> str:
        """获取节点对应的源代码"""
        return source_code[node.start_byte:node.end_byte]
    
    def _extract_name(self, node: Node, source_code: str) -> str:
        """提取节点的名称"""
        for child in node.children:
            if child.type == 'identifier':
                return self._get_node_code(child, source_code)
        return ''
    
    def _is_constant(self, node: Node) -> bool:
        """判断是否是常量定义"""
        name = self._extract_name(node, self.source_code)
        return name.isupper() and '_' in name
    
    def _process_node(self, 
                     node: Node, 
                     source_code: str, 
                     parent: Optional[str] = None) -> List[PythonCodeElement]:
        """处理单个节点"""
        elements = []
        
        if node.type == 'class_definition':
            name = self._extract_name(node, source_code)
            docstring = self._extract_docstring(node, source_code)
            class_element = PythonCodeElement(
                type='class',
                name=name,
                code=self._get_node_code(node, source_code),
                docstring=docstring,
                parent=parent,
                start_point=node.start_point,
                end_point=node.end_point
            )
            elements.append(class_element)
            
            # 处理类的方法
            for child in node.children:
                if child.type == 'block':
                    for method_node in child.children:
                        if method_node.type == 'function_definition':
                            elements.extend(self._process_node(method_node, source_code, name))
                            
        elif node.type == 'function_definition':
            name = self._extract_name(node, source_code)
            docstring = self._extract_docstring(node, source_code)
            func_type = 'method' if parent else 'function'
            func_element = PythonCodeElement(
                type=func_type,
                name=name,
                code=self._get_node_code(node, source_code),
                docstring=docstring,
                parent=parent,
                start_point=node.start_point,
                end_point=node.end_point
            )
            elements.append(func_element)
            
        elif node.type == 'assignment' and self._is_constant(node):
            name = self._extract_name(node, source_code)
            const_element = PythonCodeElement(
                type='constant',
                name=name,
                code=self._get_node_code(node, source_code),
                parent=parent,
                start_point=node.start_point,
                end_point=node.end_point
            )
            elements.append(const_element)
            
        return elements
    
    def parse_code(self, source_code: str) -> List[PythonCodeElement]:
        """解析Python源代码"""
        self.source_code = source_code
        tree = self.parser.parse(bytes(source_code, 'utf8'))
        
        elements = []
        for node in tree.root_node.children:
            elements.extend(self._process_node(node, source_code))
            
        return elements

class CodeSplitter(BaseProcessor):
    """智能代码分割处理器"""
    def __init__(self):
        self.python_parser = TreeSitterCodeParser()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
    def _process_python_file(self, file_path: str, content: str) -> List[Dict]:
        """处理Python文件"""
        code_elements = self.python_parser.parse_code(content)
        documents = []
        
        for element in code_elements:
            element_dict = element.to_dict()
            doc = {
                'content': element_dict['code'],
                'file_path': file_path,
                'element_type': element_dict['type'],
                'element_name': element_dict['name'],
                'docstring': element_dict['docstring'],
                'parent': element_dict['parent'],
                'location': element_dict['location'],
                'file_type': '.py',
                'relative_path': os.path.relpath(file_path)
            }
            documents.append(doc)
            
        return documents
    
    def _process_text_file(self, file_path: str, content: str) -> List[Dict]:
        """处理普通文本文件"""
        chunks = self.text_splitter.split_text(content)
        documents = []
        
        for i, chunk in enumerate(chunks):
            doc = {
                'content': chunk,
                'file_path': file_path,
                'chunk_id': i,
                'file_type': os.path.splitext(file_path)[1],
                'relative_path': os.path.relpath(file_path)
            }
            documents.append(doc)
            
        return documents
    
    def process(self, file_paths: List[str]) -> List[Dict]:
        """处理所有文件"""
        documents = []
        
        for file_path in file_paths:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if file_path.endswith('.py'):
                docs = self._process_python_file(file_path, content)
            else:
                docs = self._process_text_file(file_path, content)
                
            documents.extend(docs)
            
        return documents