from Codereader import CodeKnowledgeBase

# 初始化知识库
kb = CodeKnowledgeBase(openai_api_key="sk-e53cf170fff844b88f5a7e2b4c4a86d5")

# 构建知识库
kb.build_knowledge_base(
    project_path="./your_project_path",
    output_path="./code_knowledge_base"
)

# 查询
results = kb.query(
    query="查找用户认证相关的代码",
    knowledge_base_path="./code_knowledge_base"
)