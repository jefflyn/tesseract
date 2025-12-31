from graphviz import Digraph

# 创建图
dot = Digraph(comment="AI 时代后端工程师 Notion 技术知识库结构", format="png")
dot.attr(rankdir="TB", fontsize="12", fontname="Microsoft YaHei")

# 一级目录
sections = [
    "核心后端技术",
    "系统架构与高可用",
    "AI + 后端融合能力",
    "DevOps 与云原生",
    "数据与分析",
    "业务与产品理解",
    "职业发展与软技能"
]

# 二级目录映射
subsections = {
    "核心后端技术": ["Java 基础与进阶", "Spring 全家桶", "数据库与缓存", "消息队列", "分布式与微服务"],
    "系统架构与高可用": ["架构设计原则", "高并发处理", "高可用与容灾", "数据一致性", "CAP & BASE 理论", "限流/熔断/降级"],
    "AI + 后端融合能力": ["AI 工具链使用", "Prompt Engineering", "AI API 集成", "向量数据库", "AI 安全与合规", "AI 驱动的业务场景"],
    "DevOps 与云原生": ["容器化", "Kubernetes", "CI/CD", "服务监控", "日志采集", "云服务"],
    "数据与分析": ["数据建模", "实时计算", "数据仓库", "BI 工具"],
    "业务与产品理解": ["领域驱动设计", "常见业务场景", "业务建模与拆解"],
    "职业发展与软技能": ["技术写作", "团队协作与沟通", "系统复盘与总结", "技术选型与成本评估"]
}

# 根节点
dot.node("Notion", "AI 时代后端工程师\nNotion 技术知识库", shape="box", style="filled", color="lightblue")

# 添加节点
for sec in sections:
    dot.node(sec, sec, shape="folder", style="filled", color="lightgoldenrod1")
    dot.edge("Notion", sec)
    for sub in subsections[sec]:
        dot.node(f"{sec}_{sub}", sub, shape="note", color="white", style="filled")
        dot.edge(sec, f"{sec}_{sub}")

# 保存并渲染
# output_path = "/mnt/data/notion_knowledge_base"
# dot.render(output_path, cleanup=True)

# output_path + ".png"

dot.render("notion_knowledge_base", cleanup=True)