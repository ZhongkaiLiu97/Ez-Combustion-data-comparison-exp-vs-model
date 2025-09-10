import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io

# 设置中文字体支持
# 请根据你的操作系统和安装的字体选择合适的字体
# Windows: 'SimHei', 'Microsoft YaHei'
# Linux/macOS: 'Source Han Sans CN', 'WenQuanYi Zen Hei', 'Noto Sans CJK SC'
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

st.set_page_config(
    layout="wide",
    page_title="多系列数据可视化工具",
    page_icon="📊"
)

# 自定义CSS样式
# 注意：CSS样式在Streamlit的rerun中可能会“闪烁”，但通常是允许的
st.markdown("""
<style>
    .stForm {
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        background-color: rgba(255, 255, 255, 0.05);
    }
    div[data-testid="stMetricValue"] {
        font-size: 20px;
    }
    .stDataFrame {
        font-size: 14px;
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.title("📊 多系列数据可视化工具")
st.markdown("灵活添加实验与模型数据系列进行对比分析")
st.markdown("---")

# 初始化session state
initial_rows = 10
# 默认数据系列数量
if 'num_series' not in st.session_state:
    st.session_state.num_series = 3 # 初始默认显示3组X/Y数据

def generate_empty_df(num_rows, num_series):
    """根据行数和系列数生成空的DataFrame结构"""
    data = {}
    for i in range(1, num_series + 1):
        data[f'Label{i}'] = [''] * num_rows
        data[f'X{i}'] = [None] * num_rows
        data[f'Y{i}'] = [None] * num_rows
    return pd.DataFrame(data)

def ensure_columns_exist(df, min_series_num):
    """确保DataFrame包含至少min_series_num所需的列，并按序排列"""
    new_cols_df = {}
    for i in range(1, min_series_num + 1):
        label_col = f'Label{i}'
        x_col = f'X{i}'
        y_col = f'Y{i}'
        
        # 将现有数据放入新结构
        new_cols_df[label_col] = df.get(label_col, pd.Series([''] * len(df)))
        new_cols_df[x_col] = df.get(x_col, pd.Series([None] * len(df)))
        new_cols_df[y_col] = df.get(y_col, pd.Series([None] * len(df)))
        
    # 如果现有DataFrame有更多列，保留
    existing_extra_cols = [col for col in df.columns if col not in new_cols_df]
    for col in existing_extra_cols:
        new_cols_df[col] = df[col]

    return pd.DataFrame(new_cols_df)


# 初始化或更新session state的DataFrame  
# 当 num_series 改变时，确保 DataFrame 结构同步更新
if 'exp_data' not in st.session_state:
    st.session_state.exp_data = generate_empty_df(initial_rows, st.session_state.num_series)
    # 填充一些初始示例数据
    st.session_state.exp_data.iloc[0, st.session_state.exp_data.columns.get_loc('Label1')] = 'Exp-Series1'
    st.session_state.exp_data.iloc[0:5, st.session_state.exp_data.columns.get_loc('X1')] = [1.0, 2.0, 3.0, 4.0, 5.0]
    st.session_state.exp_data.iloc[0:5, st.session_state.exp_data.columns.get_loc('Y1')] = [10.0, 15.0, 13.0, 17.0, 20.0]
    st.session_state.exp_data.iloc[0, st.session_state.exp_data.columns.get_loc('Label2')] = 'Exp-Series2'
    st.session_state.exp_data.iloc[0:5, st.session_state.exp_data.columns.get_loc('X2')] = [1.5, 2.5, 3.5, 4.5, 5.5]
    st.session_state.exp_data.iloc[0:5, st.session_state.exp_data.columns.get_loc('Y2')] = [11.0, 16.0, 14.0, 18.0, 21.0]
else:
    # 确保当 num_series 变化时，已有的 DataFrame 也能适配新结构
    st.session_state.exp_data = ensure_columns_exist(st.session_state.exp_data.copy(), st.session_state.num_series)


if 'model_data' not in st.session_state:
    st.session_state.model_data = generate_empty_df(initial_rows, st.session_state.num_series)
    # 填充一些初始示例数据
    st.session_state.model_data.iloc[0, st.session_state.model_data.columns.get_loc('Label1')] = 'Model-Series1'
    st.session_state.model_data.iloc[0:5, st.session_state.model_data.columns.get_loc('X1')] = [1.0, 2.0, 3.0, 4.0, 5.0]
    st.session_state.model_data.iloc[0:5, st.session_state.model_data.columns.get_loc('Y1')] = [9.0, 14.0, 13.5, 16.8, 19.5]
    st.session_state.model_data.iloc[0, st.session_state.model_data.columns.get_loc('Label2')] = 'Model-Series2'
    st.session_state.model_data.iloc[0:5, st.session_state.model_data.columns.get_loc('X2')] = [1.5, 2.5, 3.5, 4.5, 5.5]
    st.session_state.model_data.iloc[0:5, st.session_state.model_data.columns.get_loc('Y2')] = [10.5, 15.5, 13.0, 17.5, 20.0]
else:
    st.session_state.model_data = ensure_columns_exist(st.session_state.model_data.copy(), st.session_state.num_series)


# 清空数据按钮（放在表单外）
col_series_btn1, col_series_btn2, col_clear1, col_clear2 = st.columns([0.8, 0.8, 1, 1])

with col_series_btn1:
    if st.button("➕ 增加系列", key="add_series_btn"):
        st.session_state.num_series += 1
        # 强制更新 DataFrame 结构以包含新列
        st.session_state.exp_data = ensure_columns_exist(st.session_state.exp_data, st.session_state.num_series)
        st.session_state.model_data = ensure_columns_exist(st.session_state.model_data, st.session_state.num_series)
        st.rerun()

with col_series_btn2:
    if st.session_state.num_series > 1: # 至少保留一个系列
        if st.button("➖ 减少系列", key="minus_series_btn"):
            st.session_state.num_series -= 1
            # 强制更新 DataFrame 结构以移除多余列
            st.session_state.exp_data = ensure_columns_exist(st.session_state.exp_data, st.session_state.num_series)
            st.session_state.model_data = ensure_columns_exist(st.session_state.model_data, st.session_state.num_series)
            st.rerun()
    else:
        st.button("➖ 减少系列", disabled=True, help="至少保留一组数据系列")


with col_clear1:
    if st.button("🗑️ 清空实验数据", help="重置实验数据表格"):
        st.session_state.exp_data = generate_empty_df(initial_rows, st.session_state.num_series)
        st.rerun()

with col_clear2:
    if st.button("🗑️ 清空模型数据", help="重置模型数据表格"):
        st.session_state.model_data = generate_empty_df(initial_rows, st.session_state.num_series)
        st.rerun()

# 主表单区域
with st.form("main_form"):
    st.markdown("### 📌 使用说明")
    st.info("""
    - 📋 **直接复制粘贴**：从Excel或其他表格软件复制数据，点击单元格后粘贴
    - 🔢 **增减数据系列**：点击上方的 "增加系列" 或 "减少系列" 按钮来动态调整表格中的数据列数量
    - 🏷️ **独立标签**：每组X/Y数据都有独立的标签列（例如：Label1对应X1/Y1）。你可以在标签列的第一行填写该系列的名称。
    - 📊 **数据输入**：在对应的X和Y列输入数据点。
    - ✏️ **流畅编辑**：表格编辑不会刷新页面。所有更改会在点击"生成图表"按钮后才会更新。
    - ➕ **添加行**：点击表格下方的 "+" 按钮添加更多数据行。
    """)

    # 动态生成列配置和显示顺序
    column_config = {}
    display_order = []
    for i in range(1, st.session_state.num_series + 1):
        column_config[f'Label{i}'] = st.column_config.TextColumn(
            f"标签{i}",
            help=f"第{i}组数据的标签",
            width="small",
        )
        column_config[f'X{i}'] = st.column_config.NumberColumn(f"X{i}", help=f"第{i}组X轴数据", format="%.2f")
        column_config[f'Y{i}'] = st.column_config.NumberColumn(f"Y{i}", help=f"第{i}组Y轴数据", format="%.2f")
        display_order.extend([f'Label{i}', f'X{i}', f'Y{i}'])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔬 实验数据")
        exp_df_edited = st.data_editor(
            st.session_state.exp_data,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=False,
            column_config=column_config,
            column_order=display_order,
            key="exp_editor"
        )

    with col2:
        st.subheader("📈 模型数据")
        model_df_edited = st.data_editor(
            st.session_state.model_data,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=False,
            column_config=column_config,
            column_order=display_order,
            key="model_editor"
        )

    st.markdown("---")
    st.subheader("⚙️ 图表设置")

    # 图表参数设置
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**基本设置**")
        plot_title = st.text_input("图表标题", "数据对比分析")
        x_label = st.text_input("X轴标签", "X")
        y_label = st.text_input("Y轴标签", "Y")

    with col2:
        st.markdown("**实验数据样式**")
        exp_color_scheme = st.selectbox(
            "颜色方案",
            ['暖色系', '冷色系', '彩虹色', '单色渐变'],
            key="exp_colors"
        )
        exp_marker = st.selectbox(
            "标记样式",
            ['o', 's', '^', 'D', 'v', '*', ''],
            format_func=lambda x: {
                'o': '圆形 ●', 's': '方形 ■', '^': '三角形 ▲',
                'D': '菱形 ◆', 'v': '倒三角 ▼', '*': '星形 ★',
                '': '无标记'
            }.get(x, x),
            key="exp_marker_style" # 添加key
        )
        exp_linestyle = st.selectbox(
            "线型",
            ['', '-', '--', '-.', ':'],
            format_func=lambda x: {
                '': '仅散点', '-': '实线', '--': '虚线', '-.': '点划线', ':': '点线'
            }.get(x, x),
            key="exp_linestyle_style" # 添加key
        )


    with col3:
        st.markdown("**模型数据样式**")
        model_color_scheme = st.selectbox(
            "颜色方案",
            ['冷色系', '暖色系', '彩虹色', '单色渐变'],
            key="model_colors"
        )
        model_marker = st.selectbox(
            "标记样式",
            ['', 'o', 's', '^', 'D', 'v', '*'],
            format_func=lambda x: {
                '': '无标记', 'o': '圆形 ●', 's': '方形 ■',
                '^': '三角形 ▲', 'D': '菱形 ◆',
                'v': '倒三角 ▼', '*': '星形 ★'
            }.get(x, x),
            key="model_marker_style" # 添加key
        )
        model_linestyle = st.selectbox(
            "线型",
            ['-', '--', '-.', ':', ''],
            format_func=lambda x: {
                '-': '实线', '--': '虚线', '-.': '点划线', ':': '点线', '': '仅散点'
            }.get(x, x),
            key="model_linestyle_style" # 添加key
        )

    # 高级选项
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**高级选项**")
        grid = st.checkbox("显示网格", value=True)
        legend_loc = st.selectbox("图例位置", ['best', 'upper right', 'upper left', 'lower right', 'lower left'])
        fig_size = st.slider("图表大小", 6, 15, 10)

    with col2:
        st.markdown("**显示设置**")
        show_exp = st.checkbox("显示实验数据", value=True)
        show_model = st.checkbox("显示模型数据", value=True)
        separate_plots = st.checkbox("分离显示", value=False)

    # 唯一的提交按钮
    submitted = st.form_submit_button("🎨 生成图表", type="primary", use_container_width=True)

# 数据处理函数
def prepare_data_from_table(df, current_num_series):
    """从表格中提取绘图数据，每个X/Y对有独立的标签"""
    plot_data = []
    
    for i in range(1, current_num_series + 1):  # 动态处理num_series组数据
        x_col = f'X{i}'
        y_col = f'Y{i}'
        label_col = f'Label{i}'
        
        # 仅处理实际存在的列
        if not all(col in df.columns for col in [x_col, y_col, label_col]):
            continue

        current_label = None
        x_values = []
        y_values = []
        
        for idx, row in df.iterrows():
            row_label = str(row[label_col]).strip() if pd.notna(row[label_col]) else ''
            
            # 如果是该系列的第一行，或遇到新标签
            if row_label and current_label != row_label: # 避免相同标签重复触发
                # 如果有累积的数据点，且标签不同，则保存之前的数据
                if current_label and x_values and y_values:
                    plot_data.append({
                        'label': current_label,
                        'x': x_values,
                        'y': y_values
                    })
                    x_values = [] # 重置数据点
                    y_values = []
                current_label = row_label # 更新当前标签
            
            # 收集数据点
            if current_label and pd.notna(row[x_col]) and pd.notna(row[y_col]):
                x_values.append(float(row[x_col]))
                y_values.append(float(row[y_col]))
        
        # 保存最后一组数据（处理完所有行后可能仍有未保存的数据）
        if current_label and x_values and y_values:
            plot_data.append({
                'label': current_label,
                'x': x_values,
                'y': y_values
            })
    
    return plot_data

# 颜色方案 (保持不变)
def get_color_palette(scheme):
    palettes = {
        '暖色系': ['#FF6B6B', '#FF8E53', '#FFB347', '#FFC947', '#FFD93D'],
        '冷色系': ['#6C5CE7', '#74B9FF', '#00B894', '#00CEC9', '#55A3FF'],
        '彩虹色': ['#FF6B6B', '#FFD93D', '#6BCF7F', '#4ECDC4', '#A29BFE'],
        '单色渐变': ['#2E86AB', '#48A4DB', '#69BFFC', '#7DCAFF', '#91D5FF']
    }
    return palettes.get(scheme, palettes['彩虹色'])

# 绘图逻辑
if submitted:
    # 更新session state
    st.session_state.exp_data = exp_df_edited
    st.session_state.model_data = model_df_edited
    
    # 准备数据，传入当前的系列数量
    exp_plot_data = prepare_data_from_table(exp_df_edited, st.session_state.num_series) if show_exp else []
    model_plot_data = prepare_data_from_table(model_df_edited, st.session_state.num_series) if show_model else []
    
    if not exp_plot_data and not model_plot_data:
        st.warning("⚠️ 请输入有效的数据（确保X和Y值成对，且每个系列的**第一个**数据点的标签不为空）")
    else:
        st.subheader("📊 可视化结果")
        
        # 获取颜色
        exp_colors = get_color_palette(exp_color_scheme)
        model_colors = get_color_palette(model_color_scheme)
        
        if not separate_plots:
            # 单图显示
            fig, ax = plt.subplots(figsize=(fig_size, fig_size * 0.6))
            
            # 绘制实验数据
            for i, data in enumerate(exp_plot_data):
                ax.plot(data['x'], data['y'],
                       marker=exp_marker if exp_marker else None,
                       linestyle=exp_linestyle if exp_linestyle else 'none',
                       label=data['label'],
                       color=exp_colors[i % len(exp_colors)],
                       markersize=8,
                       linewidth=2,
                       alpha=0.8)
            
            # 绘制模型数据
            for i, data in enumerate(model_plot_data):
                ax.plot(data['x'], data['y'],
                       marker=model_marker if model_marker else None,
                       linestyle=model_linestyle if model_linestyle else 'none',
                       label=data['label'],
                       color=model_colors[i % len(model_colors)],
                       markersize=6,
                       linewidth=2,
                       alpha=0.8)
            
            ax.set_xlabel(x_label, fontsize=12)
            ax.set_ylabel(y_label, fontsize=12)
            ax.set_title(plot_title, fontsize=14, fontweight='bold')
            ax.legend(loc=legend_loc)
            if grid:
                ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # 导出按钮
            col1, col2, col3 = st.columns(3)
            with col1:
                img_buffer = io.BytesIO()
                fig.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
                st.download_button(
                    "📥 下载PNG",
                    img_buffer.getvalue(),
                    f"{plot_title}.png",
                    "image/png"
                )
            
            with col2:
                svg_buffer = io.BytesIO()
                fig.savefig(svg_buffer, format='svg', bbox_inches='tight')
                st.download_button(
                    "📥 下载SVG",
                    svg_buffer.getvalue(),
                    f"{plot_title}.svg",
                    "image/svg+xml"
                )
            
            with col3:
                # 导出CSV
                all_data = exp_plot_data + model_plot_data
                if all_data:
                    export_df = pd.DataFrame()
                    for data in all_data:
                        export_df[f"{data['label']}_X"] = pd.Series(data['x'])
                        export_df[f"{data['label']}_Y"] = pd.Series(data['y'])
                    csv = export_df.to_csv(index=False)
                    st.download_button(
                        "📥 下载CSV",
                        csv,
                        f"{plot_title}_data.csv",
                        "text/csv"
                    )
            
            plt.close(fig)
            
        else:
            # 分离显示
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(fig_size * 1.5, fig_size * 0.5))
            
            # 实验数据图
            for i, data in enumerate(exp_plot_data):
                ax1.plot(data['x'], data['y'],
                        marker=exp_marker if exp_marker else None,
                        linestyle=exp_linestyle if exp_linestyle else 'none',
                        label=data['label'],
                        color=exp_colors[i % len(exp_colors)],
                        markersize=8,
                        linewidth=2,
                        alpha=0.8)
            
            ax1.set_xlabel(x_label, fontsize=11)
            ax1.set_ylabel(y_label, fontsize=11)
            ax1.set_title(f"{plot_title} - 实验数据", fontsize=12)
            if exp_plot_data:
                ax1.legend(loc=legend_loc)
            if grid:
                ax1.grid(True, alpha=0.3)
            
            # 模型数据图
            for i, data in enumerate(model_plot_data):
                ax2.plot(data['x'], data['y'],
                        marker=model_marker if model_marker else None,
                        linestyle=model_linestyle if model_linestyle else 'none',
                        label=data['label'],
                        color=model_colors[i % len(model_colors)],
                        markersize=6,
                        linewidth=2,
                        alpha=0.8)
            
            ax2.set_xlabel(x_label, fontsize=11)
            ax2.set_ylabel(y_label, fontsize=11)
            ax2.set_title(f"{plot_title} - 模型数据", fontsize=12)
            if model_plot_data:
                ax2.legend(loc=legend_loc)
            if grid:
                ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # 导出按钮
            col1, col2 = st.columns(2)
            with col1:
                img_buffer = io.BytesIO()
                fig.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
                st.download_button(
                    "📥 下载PNG",
                    img_buffer.getvalue(),
                    f"{plot_title}_separated.png",
                    "image/png"
                )
            
            with col2:
                all_data = exp_plot_data + model_plot_data
                if all_data:
                    export_df = pd.DataFrame()
                    for data in all_data:
                        export_df[f"{data['label']}_X"] = pd.Series(data['x'])
                        export_df[f"{data['label']}_Y"] = pd.Series(data['y'])
                    csv = export_df.to_csv(index=False)
                    st.download_button(
                        "📥 下载CSV",
                        csv,
                        f"{plot_title}_data.csv",
                        "text/csv"
                    )
            
            plt.close(fig)

# 底部信息
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888;'>
        <p>💡 提示：数据编辑不会刷新页面，编辑完成后点击"生成图表"按钮</p>
    </div>
    """,
    unsafe_allow_html=True
)
