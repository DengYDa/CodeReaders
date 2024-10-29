import CodeKnowledgeBase

kb = CodeKnowledgeBase(openai_api_key="your-api-key")
kb.build_knowledge_base("./your_project_path")

# 查询特定类型的代码元素
results = kb.query("查找所有与用户认证相关的类")

# 查看结果
for result in results:
    print(f"Type: {result['metadata']['element_type']}")
    print(f"Name: {result['metadata']['element_name']}")
    if result['metadata']['docstring']:
        print(f"Docstring: {result['metadata']['docstring']}")
    print(f"Code:\n{result['content']}\n")