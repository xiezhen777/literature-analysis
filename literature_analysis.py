# -*- coding: utf-8 -*-
"""
文献计量学课程作业：人工智能在教育领域的应用研究
- 模拟 CNKI 文献检索流程
- 数据清洗与导出
"""

import pandas as pd
import re

# ---------------------- 1. 检索参数配置 ----------------------
# 检索式
SEARCH_QUERY = (
    "(人工智能 OR AI OR 机器学习 OR 深度学习) "
    "AND (教育 OR 教学 OR 高等教育 OR 职业教育)"
)

# 检索条件
DATABASE = "CNKI"
TIME_RANGE = "2019-01-01 ~ 2025-12-31"
DOC_TYPE = "期刊论文"
EXCLUDE_TYPES = ["报纸", "会议", "专利", "科普", "通知"]
FINAL_COUNT = 50

# ---------------------- 2. 模拟检索与数据清洗 ----------------------
def clean_literature_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    清洗文献数据：去重、筛选、格式统一
    """
    # 1. 去重：按标题+作者去重
    df = df.drop_duplicates(subset=["标题", "作者"], keep="first")
    
    # 2. 筛选文献类型
    df = df[df["文献类型"] == DOC_TYPE]
    
    # 3. 排除无关类型
    for exclude in EXCLUDE_TYPES:
        df = df[~df["来源"].str.contains(exclude, na=False)]
    
    # 4. 年份筛选
    df["年份"] = pd.to_numeric(df["年份"], errors="coerce")
    df = df[(df["年份"] >= 2019) & (df["年份"] <= 2025)]
    
    # 5. 保留指定数量数据
    df = df.head(FINAL_COUNT)
    
    return df

# ---------------------- 3. 数据导出 ----------------------
def export_to_csv(df: pd.DataFrame, output_path: str = "csv.xlsx"):
    """
    导出清洗后的数据到 Excel/CSV
    """
    # 保留核心字段
    core_columns = ["标题", "作者", "年份", "期刊", "关键词", "被引"]
    df = df[core_columns]
    
    # 统一关键词分隔符
    df["关键词"] = df["关键词"].apply(lambda x: re.sub(r"[,，]", "；", str(x)))
    
    # 导出 Excel
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="literature_data", index=False)
    print(f"✅ 数据已导出到 {output_path}，共 {len(df)} 条记录")

# ---------------------- 4. 主函数 ----------------------
if __name__ == "__main__":
    print("📚 文献计量学作业 - 人工智能在教育领域的应用研究")
    print(f"🔍 检索式：{SEARCH_QUERY}")
    print(f"📅 时间范围：{TIME_RANGE}")
    
    # 模拟加载原始检索数据（实际场景中可替换为 CNKI 导出的 CSV）
    # 这里用你现有数据的结构模拟
    sample_data = {
        "标题": ["人工智能赋能教育变革的研究综述", "AI在高等教育中的应用现状与挑战"],
        "作者": ["张明", "李华"],
        "年份": [2020, 2021],
        "期刊": ["中国电化教育", "现代教育技术"],
        "关键词": ["人工智能；教育；赋能", "人工智能；高等教育；应用"],
        "被引": [32, 18],
        "文献类型": ["期刊论文", "期刊论文"],
        "来源": ["中国电化教育", "现代教育技术"]
    }
    df_raw = pd.DataFrame(sample_data)
    
    # 数据清洗
    df_clean = clean_literature_data(df_raw)
    
    # 导出结果
    export_to_csv(df_clean)
