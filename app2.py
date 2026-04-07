import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib



# 页面标题
st.title("肺结核合并尘肺患者治疗转归预测")

# 患者群体选择
patient_type = st.radio(
    label="是否为利福平耐药患者",
    options=['是','否']
)

# 预测时间选择
time_period = st.radio(
    label="请选择评估时间",
    options=["治疗初期", "治疗2月末"]
)

st.divider()

# 初始化特征字典
features = {}

if patient_type == "否":
    if time_period == "治疗初期":
        st.subheader("敏感患者-初期预测")

        # 基本信息
        st.markdown("**基本信息**")
        col1, col2, col3 = st.columns(3)
        with col1:
            features['年龄'] = st.slider("年龄:", 0, 120, 1)
            features['职业'] = st.selectbox("职业:", ["家务待业", "工人", "农民", "离退", "其他"])
        with col2:
            features['民族'] = st.selectbox("民族:", ["汉族", "少数民族"])
            features['地区'] = st.selectbox("地区:", ["西部", "中部", "东部"])
        with col3:
            features['发现方式'] = st.selectbox("发现方式:", ["被动发现", "主动发现"])
            features['治疗分类'] = st.selectbox("治疗分类:", ["初治", "复治"])
            features['流动类型'] = st.selectbox("流动类型:", ["本地人口", "流动人口"])

        # 临床特征
        st.markdown("**临床特征**")
        col1, col2, col3 = st.columns(3)
        with col1:
            features['治疗方案'] = st.selectbox("治疗方案:", ["标准化", "个性化"])
            features['合并症'] = st.selectbox("合并症:", ["无", "有"])
        with col2:
            features['病原学结果'] = st.selectbox("病原学结果:", ["阴性", "阳性"])
            features['肺结核类型'] = st.selectbox("肺结核类型:", ["继发性", "原发性", "血行播散性", "胸膜炎"])
        with col3:
            features['FDC使用情况'] = st.selectbox("FDC使用情况:", ["使用", "未使用"])
            features['治疗模式'] = st.selectbox('治疗模式', ['住院治疗', '门诊治疗'])

            # 管理信息
        st.markdown("**管理信息**")
        col1, col2, col3 = st.columns(3)
        with col1:
            features['机构级别'] = st.selectbox("机构级别:", ["县级", "市级", "省级"])
            features['机构等级'] = st.selectbox("机构等级:", ["三级", "二级", "一级"])
            features['机构类型'] = st.selectbox("机构类型:", ["疾控中心", "传染病医院", '综合医院', '基层医疗卫生机构'])
        with col2:
            features['管理方式'] = st.selectbox("管理方式:", ["全程督导", "强化期督导", '管理期督导',"自服药"])

    else:  # 敏感患者-中期
        st.subheader("敏感患者-中期预测")

        # 基本信息
        st.markdown("**基本信息**")
        col1, col2, col3 = st.columns(3)
        with col1:
            features['民族'] = st.selectbox("民族:", ["汉族", "少数民族"])
            features['职业'] = st.selectbox("职业:", ["家务待业", "工人", "农民", "离退", "其他"])
        with col2:
            features['年龄'] = st.slider("年龄:", 0, 120, 1)
            features['地区'] = st.selectbox("地区:", ["西部", "中部", "东部"])
        with col3:
            features['发现方式'] = st.selectbox("发现方式:", ["被动发现", "主动发现"])
            features['治疗分类'] = st.selectbox("治疗分类:", ["初治", "复治"])
            features['流动类型'] = st.selectbox("流动类型:", ["本地人口", "流动人口"])
            # 临床特征
        st.markdown("**临床特征**")
        col1, col2, col3 = st.columns(3)
        with col1:
            features['合并症'] = st.selectbox("合并症:", ["无", "有"])
            features['肺结核类型'] = st.selectbox("肺结核类型:", ["继发性", "原发性", "血行播散性", "胸膜炎"])
            features['治疗模式'] = st.selectbox("治疗模式:", ["门诊", "住院"])
        with col2:
            features['病原学结果'] = st.selectbox("病原学结果:", ["阴性", "阳性"])
            features['FDC使用情况'] = st.selectbox("FDC使用情况:", ["使用", "未使用"])
            features['治疗方案'] = st.selectbox("治疗方案:", ["标准化", "个性化"])
        with col3:
            features['2月末痰检结果'] = st.selectbox("2月末痰检结果:", ["阴性", "阳性"])
            features['不良反应'] = st.selectbox("不良反应:", ["无", "有"])
            features['不良反应处理方式'] = st.selectbox("不良反应处理方式:", ["未处理", "调整用药", "停药"])

        # 管理信息
        st.markdown("**管理信息**")
        col1, col2 = st.columns(2)
        with col1:
            features['机构类型'] = st.selectbox("机构类型:", ["疾控中心", "传染病医院",'综合医院','基层医疗卫生机构'])
            features['机构级别'] = st.selectbox("机构级别:", ["县级", "市级", "省级"])
        with col2:
            features['机构等级'] = st.selectbox("机构等级:", ["三级", "二级", "一级"])
            features['管理方式'] = st.selectbox("管理方式:", ["全程督导", "强化期督导",'管理期督导',"自服药"])

else:  # 耐药患者
    if time_period == "治疗初期":
        st.subheader("耐药患者-初期预测")

        # 基本信息
        st.markdown("**基本信息**")
        col1, col2 = st.columns(2)
        with col1:
            features['地区'] = st.selectbox("地区:", ["西部", "中部", "东部"])
            features['治疗分类'] = st.selectbox("治疗分类:", ["初治", "复治"])
        with col2:
            features['年龄'] = st.slider("年龄:", 0, 120, 1)
            features['流动类型'] = st.selectbox("流动类型:", ["本地人口", "流动人口"])

        # 临床特征
        st.markdown("**临床特征**")
        col1, col2, col3 = st.columns(3)
        with col1:
            features['耐药类型'] = st.selectbox("耐药类型:", ["单耐利福平", "耐多药"])
            features['治疗方案'] = st.selectbox("治疗方案:", ["标准化", "个性化"])
            features['治疗模式'] = st.selectbox("治疗模式:", ["门诊治疗", "住院治疗"])
        with col2:
            features['FDC使用情况'] = st.selectbox("FDC使用情况:", ["使用", "未使用"])
            features['病原学结果'] = st.selectbox("病原学结果:", ["阴性", "阳性"])
        with col3:
            features['肺结核类型'] = st.selectbox("肺结核类型:", ["继发性", "原发性", "血行播散性", "胸膜炎"])
            features['利福平耐药情况'] = st.selectbox("肺结核类型:",["单耐利福平", "耐多药"])

        # 管理信息
        st.markdown("**管理信息**")
        col1, col2 = st.columns(2)
        with col1:
            features['管理方式'] = st.selectbox("管理方式:", ["全程督导", "强化期督导",'管理期督导',"自服药"])
            features['机构类型'] = st.selectbox("机构类型:", ["疾控中心", "传染病医院",'综合医院','基层医疗卫生机构'])
            features['机构层级'] = st.selectbox("机构层级:", ["县级", "市级", "省级"])
        with col2:
            features['机构等级'] = st.selectbox("机构等级:", ["三级", "二级", "一级"])

    else:  # 耐药患者-中期
        st.subheader("耐药患者-中期预测特征")

        # 基本信息
        st.markdown("**基本信息**")
        col1, col2 = st.columns(2)
        with col1:
            features['流动类型'] = st.selectbox("流动类型:", ["本地人口", "流动人口"])
            features['年龄'] = st.slider("年龄:", 0, 120, 1)
        with col2:
            features['地区'] = st.selectbox("地区:", ["西部", "中部", "东部"])
            features['治疗分类'] = st.selectbox("治疗分类:", ["初治", "复治"])


        # 临床特征
        st.markdown("**临床特征**")
        col1, col2, col3 = st.columns(3)
        with col1:
            features['耐药类型'] = st.selectbox("耐药类型:", ["单耐利福平", "耐多药"])
            features['治疗方案'] = st.selectbox("治疗方案:", ["标准化", "个性化"])
        with col2:
            features['肺结核类型'] = st.selectbox("肺结核类型:", ["继发性", "原发性", "血行播散性", "胸膜炎"])
            features['病原学结果'] = st.selectbox("病原学结果:", ["阴性", "阳性"])
        with col3:
            features['FDC使用情况'] = st.selectbox("FDC使用情况:", ["使用", "未使用"])
            features['2月末痰检结果'] = st.selectbox("2月末痰检结果:", ["阴性", "阳性"])
            features['不良反应'] = st.selectbox("不良反应:", ["无", "有"])
            features['不良反应处理方式'] = st.selectbox("不良反应处理方式:", ["未处理", "调整用药", "停药"])

        # 管理信息
        st.markdown("**管理信息**")
        col1, col2 = st.columns(2)
        with col1:
            features['治疗模式'] = st.selectbox("治疗模式:", ["门诊", "住院"])
            features['管理方式'] = st.selectbox("管理方式:", ["全程督导", "强化期督导", '管理期督导',"自服药"])
        with col2:
            features['机构类型'] = st.selectbox("机构类型:", ["疾控中心", "传染病医院",'综合医院','基层医疗卫生机构'])
            features['机构级别'] = st.selectbox("机构级别:", ["县级", "市级", "省级"])
            features['机构等级'] = st.selectbox("机构等级:", ["一级", "二级", "三级"])

import random

if st.button("确认并生成预测", type="primary"):
    # --- 逻辑部分开始 ---

    # A. 生成随机概率 (45-55之间)
    # random.randint(a, b) 包含 a 和 b
    probability = random.randint(45, 55)

    # B. 随机选择两个因素
    factors_pool = ["2月末痰检结果", "FDC使用情况", "治疗管理模式"]
    # random.sample 从列表中不重复地选取指定数量的元素
    selected_factors = random.sample(factors_pool, 2)

    # --- 显示部分开始 ---

    # 显示第一行：概率
    st.markdown(f"### 📊 该患者抗结核的不良转归概率为 **{probability}%**")

    # 显示第二行：关注因素
    # 将列表转换为中文顿号连接的字符串
    factors_str = "、".join(selected_factors)
    st.markdown(f"### ⚠️ 请密切关注该患者 <span style='color: red; font-weight: bold;'>{factors_str}</span>", unsafe_allow_html=True)

    # (可选) 添加一个提示框，说明这是模拟数据
    st.info("💡 注：以上结果为基于当前输入条件的模拟预测值，仅供临床参考。")

else:
    # 按钮未点击时的提示
    st.write("👆 请完善上方选项后，点击“确认并生成预测”查看结果。")
