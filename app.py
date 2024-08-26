import streamlit as st
import pandas as pd
from io import StringIO

def correct_add_index():
    new_row = df.iloc[st.session_state.index].copy()
    new_row['index'] = st.session_state.index
    st.session_state.correct_data = pd.concat([st.session_state.correct_data, new_row.to_frame().T], ignore_index=True)
    st.session_state.index = min(st.session_state.index + 1, len(df) - 1)

def wrong_add_index():
    new_row = df.iloc[st.session_state.index].copy()
    new_row['index'] = st.session_state.index
    st.session_state.incorrect_data = pd.concat([st.session_state.incorrect_data, new_row.to_frame().T], ignore_index=True)
    st.session_state.index = min(st.session_state.index + 1, len(df) - 1)

def sub_index():
    st.session_state.index = max(st.session_state.index - 1, 0)
    if st.session_state.index in st.session_state.correct_data['index'].values:
        st.session_state.correct_data = st.session_state.correct_data[st.session_state.correct_data['index'] != st.session_state.index]
    if st.session_state.index in st.session_state.incorrect_data['index'].values:
        st.session_state.incorrect_data = st.session_state.incorrect_data[st.session_state.incorrect_data['index'] != st.session_state.index]

def file_upload():
    if 'index' in st.session_state:
        del st.session_state['index']
    if 'correct_data' in st.session_state:
        del st.session_state['correct_data']
    if 'incorrect_data' in st.session_state:
        del st.session_state['incorrect_data']


uploaded_file = st.file_uploader("Choose a file",on_change=file_upload)
if uploaded_file is not None:
    # To read file as bytes:
    df = pd.read_csv(uploaded_file)
    # 让用户选择要显示的列
    selected_columns = st.multiselect("选择要显示的列", df.columns)
    
    # 初始化 session state
    if 'index' not in st.session_state:
        st.session_state.index = 0
    if 'correct_data' not in st.session_state:
        st.session_state.correct_data = pd.DataFrame(columns=['index'] + list(df.columns))
    if 'incorrect_data' not in st.session_state:
        st.session_state.incorrect_data = pd.DataFrame(columns=['index'] + list(df.columns))


    # 显示当前行的数据，只显示选中的列
    st.write("数据预览：")
    if selected_columns:
        # 创建一个 DataFrame 只包含选中的列和当前行
        selected_data = df.iloc[st.session_state.index][selected_columns].to_frame().T
        st.dataframe(selected_data, width=800)
    else:
        st.write("请选择要显示的列")

    # 创建列布局
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # 处理键盘事件
    with col1:
        st.button('上一个', on_click = sub_index)

    # with col2:
    #     if st.button('下一个 (D)'):
    #         st.session_state.index = min(st.session_state.index + 1, len(df) - 1)
            #st.rerun()
    with col3:
        st.button('打标正确', on_click = correct_add_index)


    with col4:
        st.button('打标错误', on_click = wrong_add_index)



    # 下载打标数据
    st.write("打标正确的数据：")
    st.dataframe(st.session_state.correct_data)
    correct_file_name = st.text_input("输入正确的数据文件名", value="correct_data.csv")
    st.download_button("下载打标正确的数据", st.session_state.correct_data.to_csv(index=False), file_name=correct_file_name)

    st.write("打标错误的数据：")
    st.dataframe(st.session_state.incorrect_data)
    incorrect_file_name = st.text_input("输入错误的数据文件名", value="incorrect_data.csv")
    st.download_button("下载打标错误的数据", st.session_state.incorrect_data.to_csv(index=False), file_name=incorrect_file_name)
    
    # 显示打标进度
    st.sidebar.title("打标进度")
    total_rows = len(df) if uploaded_file is not None else 0
    marked_rows = len(st.session_state.correct_data) + len(st.session_state.incorrect_data)
    progress = marked_rows / total_rows if total_rows > 0 else 0
    st.sidebar.write(f"已打标个数: {marked_rows}")
    st.sidebar.write(f"总个数: {total_rows}")
    st.sidebar.progress(progress)