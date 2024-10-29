from typing import List, Dict
from .config import Config
from .core.embeddings import EmbeddingsFactory
from .core.vector_store import VectorStoreManager
from .loaders.code_loader import CodeLoader
from .processors.code_processor import CodeProcessor
from .processors.code_splitter import CodeSplitter
class CodeKnowledgeBase:
    """代码知识库主类"""
    def __init__(self, openai_api_key: str = None):
        self.config = Config()
        
        # 初始化组件
        # 初始化组件
        self.embeddings_factory = EmbeddingsFactory()
        self.vector_store_manager = VectorStoreManager()
        self.code_loader = CodeLoader(self.config.DEFAULT_FILE_EXTENSIONS)
        self.code_processor = CodeSplitter() 
        
        # 初始化向量模型
        if openai_api_key:
            self.embeddings_factory.initialize(
                embeddings_type=self.config.EMBEDDINGS_TYPE,
                openai_api_key=openai_api_key
            )
            
        # 初始化向量存储
        self.vector_store_manager.initialize(
            store_type=self.config.VECTOR_STORE_TYPE
        )
        
    def build_knowledge_base(self, project_path: str, output_path: str = 'code_knowledge_base'):
        """构建知识库"""
        # 1. 加载代码文件
        code_files = self.code_loader.load(project_path)
        
        # 2. 处理代码文件
        documents = self.code_processor.process(code_files)
        
        # 3. 创建向量存储
        texts = [doc['content'] for doc in documents]
        metadatas = [{k:v for k,v in doc.items() if k != 'content'} 
                     for doc in documents]
        
        self.vector_store_manager.create_store(
            texts=texts,
            embeddings=self.embeddings_factory.embeddings,
            metadatas=metadatas
        )
        
        # 4. 保存知识库
        self.vector_store_manager.save(output_path)
        
    def query(self, query: str, knowledge_base_path: str = 'code_knowledge_base',
             k: int = 5) -> List[Dict]:
        """查询知识库"""
        self.vector_store_manager.load(
            knowledge_base_path,
            self.embeddings_factory.embeddings
        )
        return self.vector_store_manager.search(query, k=k)