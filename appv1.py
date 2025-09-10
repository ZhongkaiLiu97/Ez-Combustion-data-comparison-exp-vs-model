import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
from matplotlib import rcParams

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(
    layout="wide", 
    page_title="数据可视化工具",
    page_icon="📊"
)

# 自定义CSS样式
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 16px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab-list"] button {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 20px;
    }
    .stDataFrame {
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.title("📊 数据可视化对比工具")
st.markdown("简洁优雅的实验数据与模型数据对比分析")
st.markdown("---")

# 初始化session state - 使用更像Excel的表格格式
if 'exp_data' not in st.session_state:
    # 创建一个10行3列的初始表格
    st.session_state.exp_data = pd.DataFrame({
        'Label': ['Exp1'] + [''] * 9,
        'X1': [1.0, 2.0, 3.0, 4.0, 5.0] + [None] * 5,
        'Y1': [10.0, 15.0, 13.0, 17.0, 20.0] + [None] * 5,
        'X2': [None] * 10,
        'Y2': [None] * 10,
        'X3': [None] * 10,
        'Y3': [None] * 10,
    })

if 'model_data' not in st.session_state:
    st.session_state.model_data = pd.DataFrame({
        'Label': ['Model1'] + [''] * 9,
        'X1': [1.0, 2.0, 3.0, 4.0, 5.0] + [None] * 5,
        'Y1': [9.0, 14.0, 13.5, 16.8, 19.5] + [None] * 5,
        'X2': [None] * 10,
        'Y2': [None] * 10,
        'X3': [None] * 10,
        'Y3': [None] * 10,
    })

# 创建三个标签页
tab1, tab2, tab3 = st.tabs(["📝 数据输入", "⚙️ 图表设置", "📊 结果展示"])

with tab1:
    st.markdown("### 📌 使用说明")
    st.info("""
    - 📋 **直接复制粘贴**：从Excel或其他表格软件复制数据，点击单元格后粘贴
    - 🏷️ **Label行**：第一行的Label用于图例显示（如 Exp1, Exp2, Model1 等）
    - 📊 **数据列**：X1/Y1 是第一组数据，X2/Y2 是第二组数据，以此类推
    - ➕ **添加行**：点击表格下方的 "+" 按钮添加更多行
    - 🗑️ **删除行**：选中行号后按Delete键删除
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔬 实验数据")
        
        # 实验数据编辑器 - 类Excel表格
        exp_df = st.data_editor(
            st.session_state.exp_data,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=False,
            column_config={
                "Label": st.column_config.TextColumn(
                    "标签",
                    help="数据集名称，将显示在图例中",
                    width="small",
                ),
                "X1": st.column_config.NumberColumn(
                    "X1",
                    help="第一组X轴数据",
                    format="%.2f",
                ),
                "Y1": st.column_config.NumberColumn(
                    "Y1",
                    help="第一组Y轴数据",
                    format="%.2f",
                ),
                "X2": st.column_config.NumberColumn(
                    "X2",
                    help="第二组X轴数据",
                    format="%.2f",
                ),
                "Y2": st.column_config.NumberColumn(
                    "Y2",
                    help="第二组Y轴数据",
                    format="%.2f",
                ),
                "X3": st.column_config.NumberColumn(
                    "X3",
                    help="第三组X轴数据",
                    format="%.2f",
                ),
                "Y3": st.column_config.NumberColumn(
                    "Y3",
                    help="第三组Y轴数据",
                    format="%.2f",
                ),
            },
            key="exp_editor"
        )
        st.session_state.exp_data = exp_df
        
        # 快速操作按钮
        ecol1, ecol2, ecol3 = st.columns(3)
        with ecol1:
            if st.button("清空实验数据", key="clear_exp"):
                st.session_state.exp_data = pd.DataFrame({
                    'Label': [''] * 10,
                    'X1': [None] * 10, 'Y1': [None] * 10,
                    'X2': [None] * 10, 'Y2': [None] * 10,
                    'X3': [None] * 10, 'Y3': [None] * 10,
                })
                st.rerun()
        
    with col2:
        st.subheader("📈 模型数据")
        
        # 模型数据编辑器 - 类Excel表格
        model_df = st.data_editor(
            st.session_state.model_data,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=False,
            column_config={
                "Label": st.column_config.TextColumn(
                    "标签",
                    help="数据集名称，将显示在图例中",
                    width="small",
                ),
                "X1": st.column_config.NumberColumn(
                    "X1",
                    help="第一组X轴数据",
                    format="%.2f",
                ),
                "Y1": st.column_config.NumberColumn(
                    "Y1",
                    help="第一组Y轴数据",
                    format="%.2f",
                ),
                "X2": st.column_config.NumberColumn(
                    "X2",
                    help="第二组X轴数据",
                    format="%.2f",
                ),
                "Y2": st.column_config.NumberColumn(
                    "Y2",
                    help="第二组Y轴数据",
                    format="%.2f",
                ),
                "X3": st.column_config.NumberColumn(
                    "X3",
                    help="第三组X轴数据",
                    format="%.2f",
                ),
                "Y3": st.column_config.NumberColumn(
                    "Y3",
                    help="第三组Y轴数据",
                    format="%.2f",
                ),
            },
            key="model_editor"
        )
        st.session_state.model_data = model_df
        
        # 快速操作按钮
        mcol1, mcol2, mcol3 = st.columns(3)
        with mcol1:
            if st.button("清空模型数据", key="clear_model"):
                st.session_state.model_data = pd.DataFrame({
                    'Label': [''] * 10,
                    'X1': [None] * 10, 'Y1': [None] * 10,
                    'X2': [None] * 10, 'Y2': [None] * 10,
                    'X3': [None] * 10, 'Y3': [None] * 10,
                })
                st.rerun()

with tab2:
    st.subheader("⚙️ 自定义图表参数")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**基本设置**")
        plot_title = st.text_input("图表标题", "数据对比分析", help="图表的主标题")
        x_label = st.text_input("X轴标签", "X", help="X轴的名称")
        y_label = st.text_input("Y轴标签", "Y", help="Y轴的名称")
        
    with col2:
        st.markdown("**实验数据样式**")
        exp_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
        exp_color_scheme = st.selectbox(
            "颜色方案", 
            ['暖色系', '冷色系', '彩虹色', '单色渐变'],
            key="exp_color_select"
        )
        exp_marker = st.selectbox(
            "标记样式", 
            ['o', 's', '^', 'D', 'v', 'p', '*', 'h'], 
            format_func=lambda x: {'o':'圆形 ●', 's':'方形 ■', '^':'三角形 ▲', 'D':'菱形 ◆', 
                                  'v':'倒三角 ▼', 'p':'五边形 ⬟', '*':'星形 ★', 'h':'六边形 ⬢'}[x],
            key="exp_marker_select"
        )
        exp_linestyle = st.selectbox(
            "线型", 
            ['', '-', '--', '-.', ':'], 
            format_func=lambda x: {'':'仅散点', '-':'实线', '--':'虚线', 
                                  '-.':'点划线', ':':'点线'}[x if x else ''],
            key="exp_line_select"
        )
        
    with col3:
        st.markdown("**模型数据样式**")
        model_colors = ['#6C5CE7', '#00B894', '#FDCB6E', '#E17055', '#74B9FF', '#A29BFE', '#55A3FF']
        model_color_scheme = st.selectbox(
            "颜色方案", 
            ['冷色系', '暖色系', '彩虹色', '单色渐变'],
            key="model_color_select"
        )
        model_marker = st.selectbox(
            "标记样式", 
            ['', 'o', 's', '^', 'D', 'v', 'p', '*'], 
            format_func=lambda x: {'':'无标记', 'o':'圆形 ●', 's':'方形 ■', '^':'三角形 ▲', 
                                  'D':'菱形 ◆', 'v':'倒三角 ▼', 'p':'五边形 ⬟', '*':'星形 ★'}[x if x else ''],
            key="model_marker_select"
        )
        model_linestyle = st.selectbox(
            "线型", 
            ['-', '--', '-.', ':', ''], 
            format_func=lambda x: {'-':'实线', '--':'虚线', '-.':'点划线', 
                                  ':':'点线', '':'仅散点'}[x if x else ''],
            key="model_line_select"
        )
    
    st.markdown("---")
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
        separate_plots = st.checkbox("分离显示（实验/模型分开）", value=False)

# 准备绘图数据 - 从表格格式提取
def prepare_data_from_table(df):
    """从表格格式提取绘图数据"""
    plot_data = []
    
    # 获取所有的标签（第一行非空的Label）
    labels = df['Label'].dropna().unique()
    
    for label in labels:
        if label and str(label).strip():  # 确保标签非空
            label_rows = df[df['Label'] == label]
            
            # 检查每组X/Y数据
            for i in range(1, 4):  # X1/Y1, X2/Y2, X3/Y3
                x_col = f'X{i}'
                y_col = f'Y{i}'
                
                if x_col in df.columns and y_col in df.columns:
                    # 提取该标签对应的所有行的X和Y数据
                    x_data = []
                    y_data = []
                    
                    for _, row in label_rows.iterrows():
                        if pd.notna(row[x_col]) and pd.notna(row[y_col]):
                            x_data.append(float(row[x_col]))
                            y_data.append(float(row[y_col]))
                    
                    # 如果是第一行的标签，还需要检查后续行是否有相同列的数据
                    first_label_idx = df[df['Label'] == label].index[0]
                    for idx in range(first_label_idx + 1, len(df)):
                        if pd.isna(df.loc[idx, 'Label']) or df.loc[idx, 'Label'] == '':
                            if pd.notna(df.loc[idx, x_col]) and pd.notna(df.loc[idx, y_col]):
                                x_data.append(float(df.loc[idx, x_col]))
                                y_data.append(float(df.loc[idx, y_col]))
                        else:
                            break  # 遇到新的标签就停止
                    
                    if x_data and y_data and len(x_data) == len(y_data):
                        plot_label = f"{label}" if i == 1 else f"{label}_{i}"
                        plot_data.append({
                            'label': plot_label,
                            'x': x_data,
                            'y': y_data
                        })
    
    return plot_data

# 获取颜色方案
def get_color_palette(scheme, n_colors=7):
    if scheme == '暖色系':
        return ['#FF6B6B', '#FF8E53', '#FF9F40', '#FFB347', '#FFC947', '#FFD93D', '#FFED4E']
    elif scheme == '冷色系':
        return ['#6C5CE7', '#5F3DC4', '#74B9FF', '#0984E3', '#00B894', '#00CEC9', '#55A3FF']
    elif scheme == '彩虹色':
        return ['#FF6B6B', '#FF9F40', '#FFD93D', '#6BCF7F', '#4ECDC4', '#74B9FF', '#A29BFE']
    else:  # 单色渐变
        return ['#2E86AB', '#3B95C3', '#48A4DB', '#55B3F3', '#69BFFC', '#7DCAFF', '#91D5FF']

with tab3:
    st.subheader("📊 可视化结果")
    
    # 生成图表按钮
    if st.button("🎨 生成图表", type="primary", use_container_width=True):
        exp_plot_data = prepare_data_from_table(st.session_state.exp_data) if show_exp else []
        model_plot_data = prepare_data_from_table(st.session_state.model_data) if show_model else []
        
        if not exp_plot_data and not model_plot_data:
            st.warning("⚠️ 请输入有效的数据（确保X和Y值成对且标签不为空）")
        else:
            # 获取颜色
            exp_colors = get_color_palette(exp_color_scheme)
            model_colors = get_color_palette(model_color_scheme)
            
            if not separate_plots:
                # 合并显示
                fig, ax = plt.subplots(figsize=(fig_size, fig_size*0.6))
                
                # 绘制实验数据
                for i, data in enumerate(exp_plot_data):
                    color = exp_colors[i % len(exp_colors)]
                    ax.plot(data['x'], data['y'], 
                           marker=exp_marker if exp_marker else None,
                           linestyle=exp_linestyle if exp_linestyle else 'none',
                           label=data['label'],
                           color=color,
                           markersize=8,
                           linewidth=2,
                           alpha=0.8)
                
                # 绘制模型数据
                for i, data in enumerate(model_plot_data):
                    color = model_colors[i % len(model_colors)]
                    ax.plot(data['x'], data['y'],
                           marker=model_marker if model_marker else None,
                           linestyle=model_linestyle if model_linestyle else 'none',
                           label=data['label'],
                           color=color,
                           markersize=6,
                           linewidth=2,
                           alpha=0.8)
                
                ax.set_xlabel(x_label, fontsize=12)
                ax.set_ylabel(y_label, fontsize=12)
                ax.set_title(plot_title, fontsize=14, fontweight='bold')
                ax.legend(loc=legend_loc, frameon=True, shadow=True, fancybox=True)
                if grid:
                    ax.grid(True, alpha=0.3, linestyle='--')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                
                plt.tight_layout()
                st.pyplot(fig)
                
                # 导出选项
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # 导出PNG
                    img_buffer = io.BytesIO()
                    fig.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', facecolor='white')
                    img_buffer.seek(0)
                    st.download_button(
                        label="📥 下载图片 (PNG)",
                        data=img_buffer,
                        file_name=f"{plot_title.replace(' ', '_')}.png",
                        mime="image/png"
                    )
                
                with col2:
                    # 导出SVG
                    svg_buffer = io.BytesIO()
                    fig.savefig(svg_buffer, format='svg', bbox_inches='tight')
                    svg_buffer.seek(0)
                    st.download_button(
                        label="📥 下载矢量图 (SVG)",
                        data=svg_buffer,
                        file_name=f"{plot_title.replace(' ', '_')}.svg",
                        mime="image/svg+xml"
                    )
                
                with col3:
                    # 导出CSV数据
                    export_df = pd.DataFrame()
                    for data in exp_plot_data + model_plot_data:
                        x_col = f"{data['label']}_X"
                        y_col = f"{data['label']}_Y"
                        export_df[x_col] = pd.Series(data['x'])
                        export_df[y_col] = pd.Series(data['y'])
                    
                    csv_buffer = io.StringIO()
                    export_df.to_csv(csv_buffer, index=False)
                    csv_buffer.seek(0)
                    st.download_button(
                        label="📥 下载数据 (CSV)",
                        data=csv_buffer.getvalue(),
                        file_name=f"{plot_title.replace(' ', '_')}_data.csv",
                        mime="text/csv"
                    )
                
                plt.close(fig)
                
            else:
                # 分离显示
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(fig_size*1.5, fig_size*0.5))
                
                # 实验数据图
                for i, data in enumerate(exp_plot_data):
                    color = exp_colors[i % len(exp_colors)]
                    ax1.plot(data['x'], data['y'],
                            marker=exp_marker if exp_marker else None,
                            linestyle=exp_linestyle if exp_linestyle else 'none',
                            label=data['label'],
                            color=color,
                            markersize=8,
                            linewidth=2,
                            alpha=0.8)
                
                ax1.set_xlabel(x_label, fontsize=11)
                ax1.set_ylabel(y_label, fontsize=11)
                ax1.set_title(f"{plot_title} - 实验数据", fontsize=12, fontweight='bold')
                if exp_plot_data:
                    ax1.legend(loc=legend_loc, frameon=True, shadow=True, fancybox=True)
                if grid:
                    ax1.grid(True, alpha=0.3, linestyle='--')
                ax1.spines['top'].set_visible(False)
                ax1.spines['right'].set_visible(False)
                
                # 模型数据图
                for i, data in enumerate(model_plot_data):
                    color = model_colors[i % len(model_colors)]
                    ax2.plot(data['x'], data['y'],
                            marker=model_marker if model_marker else None,
                            linestyle=model_linestyle if model_linestyle else 'none',
                            label=data['label'],
                            color=color,
                            markersize=6,
                            linewidth=2,
                            alpha=0.8)
                
                ax2.set_xlabel(x_label, fontsize=11)
                ax2.set_ylabel(y_label, fontsize=11)
                ax2.set_title(f"{plot_title} - 模型数据", fontsize=12, fontweight='bold')
                if model_plot_data:
                    ax2.legend(loc=legend_loc, frameon=True, shadow=True, fancybox=True)
                if grid:
                    ax2.grid(True, alpha=0.3, linestyle='--')
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                
                plt.tight_layout()
                st.pyplot(fig)
                
                # 导出选项
                col1, col2 = st.columns(2)
                with col1:
                    img_buffer = io.BytesIO()
                    fig.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', facecolor='white')
                    img_buffer.seek(0)
                    st.download_button(
                        label="📥 下载图片 (PNG)",
                        data=img_buffer,
                        file_name=f"{plot_title.replace(' ', '_')}_separated.png",
                        mime="image/png"
                    )
                
                with col2:
                    # 导出CSV数据
                    export_df = pd.DataFrame()
                    for data in exp_plot_data + model_plot_data:
                        x_col = f"{data['label']}_X"
                        y_col = f"{data['label']}_Y"
                        export_df[x_col] = pd.Series(data['x'])
                        export_df[y_col] = pd.Series(data['y'])
                    
                    csv_buffer = io.StringIO()
                    export_df.to_csv(csv_buffer, index=False)
                    csv_buffer.seek(0)
                    st.download_button(
                        label="📥 下载数据 (CSV)",
                        data=csv_buffer.getvalue(),
                        file_name=f"{plot_title.replace(' ', '_')}_data.csv",
                        mime="text/csv"
                    )
                
                plt.close(fig)

# 底部信息
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888;'>
        <p>💡 使用提示：直接在表格中粘贴数据，像使用Excel一样方便</p>
        <p>Made with ❤️ using Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
