import streamlit as st
import pandas as pd
import sqlite3
import json
from datetime import datetime
import plotly.express as px
import io
import base64
import os
from pathlib import Path

st.markdown("""
<style>
    [data-testid="stHeader"] {
        background-color: #c0c0c0;
        font-family: 'Arial Black';
        font-size: 10px;
        color: #1e3a5f;
    }
    [data-testid="stMain"] {
        background-color: #c0c0c0;
    }
    [data-testid="stMainBlockContainer"] p{
        font-family: 'Arial Black';
        font-size: 18px;
        color: #1e3a5f;
    }
    [data-testid="stMainBlockContainer"] button {
        font-family: 'Arial Black';
        font-size: 18px;
        color: #1e3a5f;
        background-color: #d6f2f0;
        border-color: #1e3a5f;
    }
    [data-testid="stMainBlockContainer"] button:active {
        color: #1e3a5f;
        background-color: #ccccff;
        border-color: #1e3a5f;
    }
    [data-testid="stSidebar"] button {
        font-family: 'Arial Black';
        font-size: 18px;
        color: #1e3a5f;
        background-color: #d6f2f0;
        border-color: #1e3a5f;
    }
    [data-testid="stSidebar"] button:active {
        color: #1e3a5f;
        background-color: #ccccff;
        border-color: #1e3a5f;
    }
    [data-testid="stMetricValue"] p {
        font-family: 'Arial Black';
        font-size: 32px;
        color: #1e3a5f;
        text-align: left !important;
    }
    [data-testid="stExpander"] details{
        background-color: #0b132b;
    }
    [data-testid="stExpander"] details > div{
        background-color: #bbbbbb;
    }
    [data-testid="stExpander"] details > div p{
        font-family: 'Arial Black';
        font-size: 18px;
        color: #1e3a5f;
    }
    [data-testid="stExpander"] details:hover{
        border-color: #f5f5f5;
    }
    [data-testid="stExpander"] p{
        font-family: 'Arial Black';
        font-size: 18px;
        color: #f5f5f5;
    }
    [data-testid="stSidebar"] h1 {
        font-family: 'Arial Black', sans-serif !important;
        font-size: 28px !important;
        color: #1e3a5f !important;
        text-align: center !important;
        border-bottom: 3px !important;
        padding-bottom: 15px !important;
        margin-bottom: 20px !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }
    [data-testid="stSidebar"] h2 {
        font-family: 'Arial Black', sans-serif !important;
        font-size: 18px !important;
        color: #1e3a5f !important;
        text-align: center !important;
        border-bottom: 3px !important;
        padding-bottom: 15px !important;
        margin-bottom: 20px !important;
        text-transform: uppercase !important;
    }
    
    [data-testid="stMultiSelect"] p {
        font-family: 'Arial Black', sans-serif !important;
        font-size: 13px !important;
        color: #1e3a5f !important;
        text-transform: uppercase !important;
    }
    [data-testid="stMultiSelect"] [data-baseweb="tag"] {
        color: #1e3a5f !important;
        background-color: #d6f2f0;
    }
    [data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
        background-color: #0b132b;
    }
    [data-testid="stMultiSelect"] div[data-baseweb="select"] > div:hover {
        border-color: #f5f5f5;
    }
    [data-testid="stSelectboxVirtualDropdown"] {
        background-color: #0b132b;
        border-color: #f5f5f5;
        color: #1e3a5f !important;
    }
    [data-baseweb="input"] {
        background-color: #0b132b;
        color: #1e3a5f !important;
    }
    [data-baseweb="input"]:hover {
        border-color: #f5f5f5;
    }
    [data-baseweb="calendar"] {
        background-color: #0b132b;
        border-color: #f5f5f5;
        color: #1e3a5f !important;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover {
        border-color: #f5f5f5;
    }
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #0b132b;
        color: #f5f5f5 !important;
    }
    [data-testid="stTextInput"] div[data-baseweb="base-input"] > div :hover {
        border-color: #f5f5f5;
    }
    [data-testid="stMainBlockContainer"] input {
        background-color: #0b132b;
        color: #f5f5f5 !important;
    }
    [data-testid="stAlertContainer"]  [data-testid="stMarkdownContainer"] p {
        font-family: 'Arial Black', sans-serif !important;
        font-size: 16px !important;
        color: #0b132b !important;
    }
    [data-testid="stAlertContainer"]  [data-baseweb="notification"] {
        border-color: #7f2e3a !important;
    }
    [data-testid="stSelectboxVirtualDropdownEmpty"]{
        background-color: #0b132b;
        border-color: #f5f5f5;
    }
    [data-testid="stSidebar"] .stDateInput p {
        font-family: 'Arial Black', sans-serif !important;
        font-size: 13px !important;
        color: #1e3a5f !important;
        text-transform: uppercase !important;
    }
    [data-testid="stSidebar"] .stSelectbox p {
        font-family: 'Arial Black', sans-serif !important;
        font-size: 13px !important;
        color: #1e3a5f !important;
        text-transform: uppercase !important;
    }
    [data-testid="stSidebar"].element-container {
        font-family: 'Arial Black', sans-serif !important;
        font-size: 18px !important;
        color: #1e3a5f !important;
        text-transform: uppercase !important;
    }
    [data-testid="stSidebar"] {
        background-color: #c0c0c0;
    }
    [data-testid="stSidebar"] hr {
        border: 2px solid #1e3a5f;
        border-radius: 5px;
    }
    [data-testid="stSidebar"] .stRadio p {
        font-family: 'Arial Black' !important;
        font-size: 18px !important;
        color: #1e3a5f !important;
    }
    [data-testid="stMainBlockContainer"] {
        background-color: #c0c0c0;
    }
    [data-testid="stMainBlockContainer"] h1{
        font-family: 'Arial Black', sans-serif !important;
        font-size: 44px !important;
        color: #1e3a5f !important;
    }
    [data-testid="stMainBlockContainer"] h2{
        font-family: 'Arial Black', sans-serif !important;
        font-size: 32px !important;
        color: #1e3a5f !important;
    }
    [data-testid="stMainBlockContainer"] h3{
        font-family: 'Arial Black', sans-serif !important;
        font-size: 32px !important;
        color: #1e3a5f !important;
    }
    [data-testid="stMainBlockContainer"] hr {
        border: 2px solid #1e3a5f;
        border-radius: 5px;
    }
    
    [class="main-svg"] {
        
    }
</style>
""", unsafe_allow_html=True)

DB_PATH = 'quality_control.db'
TEMP_EXCEL = 'temp_asq.xlsx'

def download_db_button():
    if Path(DB_PATH).exists():
        with open(DB_PATH, 'rb') as f:
            db_bytes = f.read()
        st.sidebar.download_button(
            label = "Скачать базу данных",
            data=db_bytes,
            file_name=f"quality_control_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
            mime="application/octet-stream",
            use_container_width=True
        )
        return True
    else:
        st.sidebar.warning("Файл не найден")
        return False

def init_db(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS category (
                        id_cat INTEGER PRIMARY KEY AUTOINCREMENT,
                        name_cat TEXT NOT NULL
                        )
                ''')
    conn.execute('''CREATE TABLE IF NOT EXISTS product_types (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category INTEGER,
                        zipper INTEGER,
                        button INTEGER,
                        velcro INTEGER,
                        filler INTEGER,
                        FOREIGN KEY (category) REFERENCES category (id_cat)
                        )
                ''')
    conn.execute('''CREATE TABLE IF NOT EXISTS question (
                        id_q INTEGER PRIMARY KEY AUTOINCREMENT,
                        question TEXT NOT NULL,
                        form INTEGER,
                        category_q INTEGER
                        )
                ''')
    conn.execute('''CREATE TABLE IF NOT EXISTS category_mat (
                        id_cat_mat INTEGER PRIMARY KEY AUTOINCREMENT,
                        name_cat_mat TEXT NOT NULL
                        )
                ''')
    conn.execute('''CREATE TABLE IF NOT EXISTS materials (
                        id_mat INTEGER PRIMARY KEY AUTOINCREMENT,
                        name_mat TEXT NOT NULL,
                        category_mat INTEGER,
                        FOREIGN KEY (category_mat) REFERENCES category_mat (id_cat_mat)
                        )
                ''')
    conn.execute('''CREATE TABLE IF NOT EXISTS inspections (
                        id_in INTEGER PRIMARY KEY AUTOINCREMENT,
                        form_control INTEGER,
                        batch_number TEXT,
                        product_type_id INTEGER,
                        material_id INTEGER,
                        inspector_name TEXT,
                        inspector_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        status INTEGER
                        )
                ''')
    conn.execute('''CREATE TABLE IF NOT EXISTS inspection_answer (
                    id_in INTEGER,
                    question_id INTEGER,
                    answer INTEGER,
                    PRIMARY KEY (id_in, question_id)
                    )
            ''')
    
    conn.commit()
    return conn
    
def load_data_from_excel(conn, excel_file):
    try:
        file = pd.ExcelFile(excel_file)
        if 'category' in file.sheet_names:
            df_category = file.parse('category')
            df_category.to_sql('category', conn, if_exists='replace', index = False)
        if 'product_type' in file.sheet_names:
            df_category = file.parse('product_type')
            df_category.to_sql('product_types', conn, if_exists='replace', index = False)
        if 'question' in file.sheet_names:
            df_category = file.parse('question')
            df_category.to_sql('question', conn, if_exists='replace', index = False)
        if 'materials_category' in file.sheet_names:
            df_category = file.parse('category_mat')
            df_category.to_sql('materials_category', conn, if_exists='replace', index = False)
        if 'materials' in file.sheet_names:
            df_category = file.parse('materials')
            df_category.to_sql('materials', conn, if_exists='replace', index = False)
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Ошибка загрузки Excel: {e}")
        return False

def setup_database():
    if not Path(DB_PATH).exists():
        st.warning("База данных не найдена. Загрузить файл quality_control.db или создайте новую из Excel")
        option = st.radio("Выберите действие:", ["Загрузить готовую БД", "Создать из Excel-справочников"])
        if option == "Загрузить готовую БД":
            uploaded_db = st.file_uploader("Загрузите БД", type=['db'])
            if uploaded_db:
                with open(DB_PATH, 'wb') as f:
                    f.write(uploaded_db.getbuffer())
                st.success("База данных загружена!")
                st.rerun()
        else:
            st.info("Загрузите Excel-файл со справочниками")
            uploaded_excel = st.file_uploader("Загрузить справочники", type=['xlsx'])
            if uploaded_excel:
                with open(TEMP_EXCEL, "wb") as f:
                    f.write(uploaded_excel.getbuffer())
                conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)
                conn.execute("PRAGMA foreign_keys = ON")
                conn.execute("PRAGMA journal_mode = WAL")
                conn = init_db(conn)
                
                if load_data_from_excel(conn, TEMP_EXCEL):
                    st.success("База данных загружена!")
                    if os.path.exists(TEMP_EXCEL):
                        os.remove(TEMP_EXCEL)
                    st.rerun()
                conn.close()
                
    if Path(DB_PATH).exists():
        conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        table_count = cursor.fetchone()[0]
        if table_count < 7:
            st.warning("Структура БД неполная. Создаем таблицы")
            conn = init_db(conn)
        return conn
    return None
    
def create_checklist(conn, required_form, results):
    all_question_df = pd.read_sql("SELECT * FROM question", conn)
    question_df = all_question_df.loc[all_question_df['form'].isin(required_form)]
    st.subheader("Чек-лист качества")
    i = 1
    for i, row in question_df.iterrows():
        question_id = row['id_q']
        question_text = row['question']
        question_cat = row['category_q']
        if question_cat == 0:
            st.markdown(f"**{i+1}. {question_text}**")
            answer = st.radio(f"Ответ", ["Да", "Нет"], key=f"q_{question_id}")
            if answer == "Да":
                results[question_id] = 1
            else:
                results[question_id] = 0
        elif question_cat == 1:
            answer = st.text_input(f"**{i+1}. {question_text}**", key=f"q_{question_id}")
            results[question_id] = answer
    return results
    
def save_result(conn, form, batch, prod_id, mat_id, name, res):
    cursor = conn.cursor()
    if 0 in res.values():
        status = 0
    else:
        status = 1
    cursor.execute('''INSERT INTO inspections (form_control, batch_number, product_type_id, material_id, inspector_name, status) VALUES (?, ?, ?, ?, ?, ?)''', (form, batch, prod_id, mat_id, name, status))
    inspections_id = cursor.lastrowid
    for question_id, answer in res.items():
        cursor.execute('''INSERT INTO inspection_answer (id_in, question_id, answer) VALUES (?, ?, ?)''', (inspections_id, question_id, answer))
    conn.commit()
    st.success(f"Результаты сохранены! ID проверки: {inspections_id}")
    return inspections_id
    
def archive_page(conn):
    query = """
    SELECT
        i.id_in,
        i.batch_number,
        i.inspector_name,
        i.inspector_date,
        i.status,
        i.form_control,
        pt.name as product_name,
        m.name_mat as material_name,
        ia.question_id,
        ia.answer,
        q.question as question_text
    FROM inspections i
    LEFT JOIN product_types pt ON i.product_type_id = pt.id
    LEFT JOIN materials m ON i.material_id = m.id_mat
    LEFT JOIN inspection_answer ia ON i.id_in = ia.id_in
    LEFT JOIN question q ON ia.question_id = q.id_q
    ORDER BY i.inspector_date DESC
    """
    
    df = pd.read_sql(query, conn)
    if df.empty:
        st.info("Архив проверок пуст")
        return
    st.sidebar.header("Фильтры архива")
    control_types = {
        0: "Входной контроль",
        1: "Операционный контроль (раскрой)",
        2: "Операционный контроль (пошив)",
        3: "Приёмочный контроль"
    }
    selected_control = st.sidebar.multiselect("Тип контроля", options=list(control_types.values()), default=list(control_types.values()))
    inspectors = sorted(df['inspector_name'].dropna().unique().tolist())
    selected_inspectors = st.sidebar.multiselect("Инспектор", options=inspectors, default=inspectors[:5] if len(inspectors)>5 else inspectors)
    
    min_date = df['inspector_date'].min()
    max_date = df['inspector_date'].max()
    
    date_range = st.sidebar.date_input("Период", value=[min_date, max_date], min_value = min_date, max_value = max_date)
    filtered_df = df.copy()
    
    selected_codes = [k for k, v in control_types.items() if v in selected_control]
    filtered_df = filtered_df[filtered_df['form_control'].isin(selected_codes)]
    
    if selected_inspectors:
        filtered_df = filtered_df[filtered_df['inspector_name'].isin(selected_inspectors)]
    if len(date_range) == 2:
        filtered_df['inspector_date'] = pd.to_datetime(filtered_df['inspector_date'])
        filtered_df = filtered_df[(filtered_df['inspector_date'] >= pd.Timestamp(date_range[0])) & (filtered_df['inspector_date'] >= pd.Timestamp(date_range[0]))]
        
    def format_control_type(code):
        return control_types.get(code, f"Неизвестный ({code})")
        
    def format_status(status):
        status_map = {0: "Брак", 1: "Не брак"}
        return status_map.get(status, f"Неизвестный ({status})")
    
    def format_answer(answer):
        if answer == 1:
            return "Да"
        elif answer == 0:
            return "Нет"
        elif pd.isna(answer):
            return "Нет ответа"
        else:
            return str(answer)
            
    grouped = filtered_df.groupby('id_in')
    
    for inspection_id, group in grouped:
        first_row = group.iloc[0]
        with st.expander(f"Проверка #{inspection_id} - {first_row['batch_number']}", expanded=False):
            st.write(f"Тип контроля:  {format_control_type(first_row['form_control'])}")
            st.write(f"Партия:  {first_row['batch_number']}")
            st.write(f"Инспектор:  {first_row['inspector_name']}")
            st.write(f"Дата:  {first_row['inspector_date'].strftime('%d.%m.%Y %H:%M')}")
            st.write(f"Статус:  {format_status(first_row['status'])}")
            if pd.notna(first_row['product_name']):
                st.write(f"Изделие:  {first_row['product_name']}")
            if pd.notna(first_row['material_name']):
                st.write(f"Материал:  {first_row['material_name']}")
            st.markdown("---")
            
            st.subheader("Вопросы и ответы")
            question_df = group[['question_text', 'answer']].copy()
            question_df['Ответ'] = question_df['answer'].apply(format_answer)
            question_df = question_df.rename(columns={'question_text': 'Вопрос'})
            st.dataframe(question_df[['Вопрос', 'Ответ']], hide_index=True, width='stretch', column_config={"Вопрос": st.column_config.TextColumn(width="large"), "Ответ": st.column_config.TextColumn(width="small")})
            total = len(question_df)
            yes_count = (question_df['answer']==1).sum()
            no_count = (question_df['answer']==0).sum()
            col1,col2, col3 = st.columns(3)
            with col1:
                st.metric("Всего вопросов", total)
            with col2:
                st.metric("Положительных ответов", yes_count)
            with col3:
                st.metric("Отрицательных ответов", no_count)
    st.markdown("---")
    st.subheader("Сводка архива")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Всего проверок", filtered_df['id_in'].nunique())
    with col2:
        st.metric("Успешных", filtered_df.groupby('id_in')['status'].first().eq(1).sum())
    with col3:
        st.metric("С дефектами", filtered_df.groupby('id_in')['status'].first().eq(0).sum())
    
    st.markdown("---")
    st.subheader("Экспорт данных")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Экспорт CSV", width='stretch'):
            csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(label="Скачать CSV", data=csv, file_name=f"{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", width='stretch')
    with col2:
        if st.button("Экспорт Excel", width='stretch'):
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                filtered_df.to_excel(writer, sheet_name='checks', index=False)
            excel_buffer.seek(0)
            st.download_button(label="Скачать Excel", data=excel_buffer, file_name=f"{datetime.now().strftime('%Y%m%d')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", width='stretch')
            
def analysis_page(conn):
    st.title("Анализ качества")
    query = """
    SELECT
        i.*,
        pt.name as product_name,
        m.name_mat as material_name
    FROM inspections i
    LEFT JOIN product_types pt ON i.product_type_id = pt.id
    LEFT JOIN materials m ON i.material_id = m.id_mat
    ORDER BY i.inspector_date DESC
    """
    df = pd.read_sql(query, conn)
    if df.empty:
        st.info("Архив проверок пуст")
        return
    st.sidebar.header("Фильтры анализа")
    control_types = {
        0: "Входной контроль",
        1: "Операционный контроль (раскрой)",
        2: "Операционный контроль (пошив)",
        3: "Приёмочный контроль"
    }
    selected_control = st.sidebar.multiselect("Тип контроля", options=list(control_types.values()), default=list(control_types.values()))
    inspectors = sorted(df['inspector_name'].dropna().unique().tolist())
    selected_inspectors = st.sidebar.multiselect("Инспектор", options=inspectors, default=inspectors[:5] if len(inspectors)>5 else inspectors)
    products = sorted(df['product_name'].dropna().unique().tolist())
    selected_products = st.sidebar.multiselect("Изделие", options=products, default=[])
    materials = sorted(df['material_name'].dropna().unique().tolist())
    selected_materials = st.sidebar.multiselect("Материал", options=materials, default=[])
    min_date = df['inspector_date'].min()
    max_date = df['inspector_date'].max()
    
    date_range = st.sidebar.date_input("Период", value=[min_date, max_date], min_value = min_date, max_value = max_date)
    status_options = ["Все", "Только успешные", "Только с браком"]
    selected_status = st.sidebar.selectbox("Статус", status_options)
    
    filtered_df = df.copy()
    selected_codes = [k for k, v in control_types.items() if v in selected_control]
    if selected_codes:
        filtered_df = filtered_df[filtered_df['form_control'].isin(selected_codes)]
    
    if selected_inspectors:
        filtered_df = filtered_df[filtered_df['inspector_name'].isin(selected_inspectors)]
        
    if selected_products:
        filtered_df = filtered_df[filtered_df['product_name'].isin(selected_products)]
        
    if selected_materials:
        filtered_df = filtered_df[filtered_df['material_name'].isin(selected_materials)]
        
    if len(date_range) == 2:
        filtered_df['inspector_date'] = pd.to_datetime(filtered_df['inspector_date'])
        filtered_df = filtered_df[(filtered_df['inspector_date'] >= pd.Timestamp(date_range[0])) & (filtered_df['inspector_date'] >= pd.Timestamp(date_range[0]))]
    
    if selected_status == "Только успешные":
        filtered_df = filtered_df[filtered_df['status'] == 1]
    elif selected_status == "Только с браком":
        filtered_df = filtered_df[filtered_df['status'] == 0]
        
    st.markdown("---")
    
    analysis_type = st.selectbox("Выберите тип анализа:", ["Общая статистика", "Динамика по времени", "Анализ по изделиям", "Анализ по материалам"])
    filtered_df['inspector_date']=pd.to_datetime(filtered_df['inspector_date'])
    filtered_df['date'] = filtered_df['inspector_date'].dt.date
    filtered_df['week'] = filtered_df['inspector_date'].dt.strftime('%Y-%W')
    filtered_df['month'] = filtered_df['inspector_date'].dt.strftime('%Y-%m')
    filtered_df['control_type_name'] = filtered_df['form_control'].map(control_types)
    filtered_df['status_name'] = filtered_df['status'].map({1: "Не брак", 0: "Брак"})
    if analysis_type == "Общая статистика":
        show_general_stats(filtered_df)
    elif analysis_type == "Динамика по времени":
        show_time_dynamics(filtered_df)
    elif analysis_type == "Анализ по изделиям":
        show_product_analysis(filtered_df)
    elif analysis_type == "Анализ по материалам":
        show_material_analysis(filtered_df)
        
def show_general_stats(df):
    st.header("Общая статистика")
    total = len(df)
    success = len(df[df['status'] == 1])
    defects = len(df[df['status'] == 0])
    defect_rate = (defects / total * 100) if total > 0 else 0
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Всего проверок", total)
    with col2:
        st.metric("Успешных", success)
    with col3:
        st.metric("С браком", defects)
    st.markdown("---")
    st.subheader("По типам контроля")
    control_counts = df['control_type_name'].value_counts()
    fig = px.pie(values = control_counts.values, names = control_counts.index, color_discrete_sequence = px.colors.qualitative.Set3)
    st.plotly_chart(fig, width='stretch')
    
    st.subheader("Соотношение успешных/брак")
    status_counts = df['status_name'].value_counts()
    fig = px.pie(values = status_counts.values, names = status_counts.index, color = status_counts.index, color_discrete_map = {"Успешно": "green", "Брак": "red"})
    st.plotly_chart(fig, width='stretch')
        
def show_time_dynamics(df):
    st.header("Динамика качества по времени")
    group_by = st.radio("Группировать по:", ["По дням", "По неделям", "По месяцам"], horizontal=True)
    if group_by == "По дням":
        group_col = 'date'
    elif group_by == "По неделям":
        group_col = 'week'
    else:
        group_col = 'month'
        
    time_stats = df.groupby(group_col).agg(total=('id_in', 'count'), success=('status',lambda x: (x==1).sum()), defects=('status',lambda x: (x==0).sum())).reset_index()
    time_stats['defect_rate'] = (time_stats['defects']/time_stats['total']*100).round(1)
    st.subheader("Количество проверок")
    fig1 = px.line(time_stats, x=group_col, y=['total', 'success', 'defects'], labels={'value': 'Количество', 'variable': 'Тип'}, color_discrete_map={'total': 'blue', 'success': 'green', 'defects': 'red'})
    st.plotly_chart(fig1, width='stretch')
    
    st.subheader("Процент брака")
    fig2 = px.line(time_stats, x=group_col, y='defect_rate', labels={'defect_rate': 'Процент брака, %'})
    fig2.update_traces(line_color='orange', line_width=3)
    fig2.add_hline(y=time_stats['defect_rate'].mean(), line_dash="dash", line_color="gray")
    st.plotly_chart(fig2, width='stretch')
    
    
def show_product_analysis(df):
    st.header("Анализ по изделиям")
    if df['product_name'].nunique() == 0:
        st.info("Нет данных по изделиям")
        return
    products = df['product_name'].dropna().unique()
    selected_products = st.multiselect("Выберите изделия для сравнения:", options=products, default=products[:3] if len(products) > 3 else products)
    if not selected_products:
        st.info("Выберите изделия для анализа")
        return
    
    product_df = df[df['product_name'].isin(selected_products)]
    product_stats = product_df.groupby('product_name').agg(total_checks=('id_in', 'count'),  success_count=('status',lambda x: (x==1).sum()), defects_count=('status',lambda x: (x==0).sum()), defect_rate=('status',lambda x: (x==0).mean()*100)).round(2).reset_index()
    
    st.subheader("Количество проверок")
    fig = px.bar(product_stats, x='product_name', y='total_checks', color='total_checks', labels={'total_checks': 'Количество проверок', 'product_name': 'Изделие'})
    st.plotly_chart(fig, width='stretch')
    
    st.subheader("Процент брака")
    fig = px.bar(product_stats, x='product_name', y='defect_rate', color='defect_rate', color_continuous_scale='RdYlGn_r', labels={'defect_rate': 'Процент брака, %', 'product_name': 'Изделие'})
    st.plotly_chart(fig, width='stretch')
    
    st.subheader("Детальная статистика")
    st.dataframe(product_stats, column_config={"product_name": "Изделие", "total_checks": "Всего проверок", "success_count": "Успешных", "defects_count": "С браком", "defect_rate": st.column_config.NumberColumn("% брака", format="%.1f%")}, hide_index=True, width='stretch')

def show_material_analysis(df):
    st.header("Анализ по материалам")
    if df['material_name'].nunique() == 0:
        st.info("Нет данных по материалам")
        return
    materials = df['material_name'].dropna().unique()
    selected_materials = st.multiselect("Выберите материалы для сравнения:", options=materials, default=materials[:3] if len(materials) > 3 else materials)
    if not selected_materials:
        st.info("Выберите материалы для анализа")
        return
    material_df = df[df['material_name'].isin(selected_materials)]
    material_stats = material_df.groupby('material_name').agg(total_checks=('id_in', 'count'), success_count=('status',lambda x: (x==1).sum()), defects_count=('status',lambda x: (x==0).sum()), defect_rate=('status',lambda x: (x==0).mean()*100)).round(2).reset_index()
    
    st.subheader("Количество проверок")
    fig = px.bar(material_stats, x='material_name', y='total_checks', color='total_checks', labels={'total_checks': 'Количество проверок', 'material_name': 'Материал'})
    st.plotly_chart(fig, width='stretch')
    
    st.subheader("Процент брака")
    fig = px.bar(material_stats, x='material_name', y='defect_rate', color='defect_rate', color_continuous_scale='RdYlGn_r', labels={'defect_rate': 'Процент брака, %', 'material_name': 'Материал'})
    st.plotly_chart(fig, width='stretch')
    
    st.subheader("Детальная статистика")
    st.dataframe(material_stats, column_config={"product_name": "Материал", "total_checks": "Всего проверок", "success_count": "Успешных", "defects_count": "С браком", "defect_rate": st.column_config.NumberColumn("% брака", format="%.1f%")}, hide_index=True, width='stretch')

st.set_page_config(page_title="Система конроля качества на ООО Метелица")

conn = setup_database()

if conn is None:
    st.info("Загрузите БД")
    st.stop()

st.sidebar.title("Система контроля качества ООО «Метелица»")
st.sidebar.markdown("___")

menu = st.sidebar.radio("Меню", ["Новая проверка", "Анализ качества", "Архив проверок"])
st.sidebar.markdown("---")
download_db_button()
st.sidebar.markdown("---")
if menu == "Новая проверка":
    st.title("Проверка качества изделия")
    col1, col2 = st.columns(2)
    with col1:
        selected_mat = ''
        selected_product = ''
        form_of_control = st.selectbox("Выберите форму контроля", ["Входной контроль", "Операционный контроль (раскрой)", "Операционный контроль (пошив)", "Приёмочный контроль"])
        if form_of_control == "Входной контроль":
            mat_category_df = pd.read_sql("SELECT id_cat_mat, name_cat_mat FROM materials_category", conn)
            mat_category_names = mat_category_df['name_cat_mat'].tolist()
            selected_mat_cat = st.selectbox("Выберите категорию материала", mat_category_names)
            selected_mat_cat_id = mat_category_df.loc[mat_category_df['name_cat_mat'] == selected_mat_cat, 'id_cat_mat'].values[0]
            materials_df = pd.read_sql("SELECT * FROM materials", conn)
            materials_with_cat = materials_df.loc[materials_df['category_mat'] == selected_mat_cat_id]
            material_names = materials_with_cat['name_mat'].tolist()
            selected_mat = st.selectbox("Выберите материал", material_names)
            batch_number = st.text_input("Номер партии", placeholder = "1234")
        if form_of_control == "Операционный контроль (раскрой)" or form_of_control == "Операционный контроль (пошив)" or form_of_control == "Приёмочный контроль":
            prod_category_df = pd.read_sql("SELECT id_cat, name_cat FROM category", conn)
            prod_category_names = prod_category_df['name_cat'].tolist()
            selected_cat = st.selectbox("Выберите категорию изделия", prod_category_names)
            selected_cat_id = prod_category_df.loc[prod_category_df['name_cat'] == selected_cat, 'id_cat'].values[0]
            product_df = pd.read_sql("SELECT * FROM product_types", conn)
            product_with_cat = product_df.loc[product_df['category'] == selected_cat_id]
            product_names = product_with_cat['name'].tolist()
            selected_product = st.selectbox("Выберите изделие", product_names)
            batch_number = st.text_input("Номер партии", placeholder = "1234")
        inspector_name = st.text_input("Ваше имя", placeholder = "Иванов Иван Иванович")
    with col2:
        if inspector_name == '':
            st.error("Введите имя")
        if batch_number == '':
            st.error("Введите номер партии")
        if form_of_control == "Входной контроль" and inspector_name != '':
            st.info(f"Выбрано для проверки {selected_mat}")
            cursor = conn.cursor()
            cursor.execute("SELECT id_mat FROM materials WHERE name_mat = ?", (selected_mat,))
            mat_id = cursor.fetchone()[0]
            results = {}
            results = create_checklist(conn, [1], results)
            if st.button("Сохранить результат"):
                save_result(conn, 0, batch_number, None, mat_id, inspector_name, results)
                st.success("Результат сохранен")
            
        if form_of_control == "Операционный контроль (раскрой)" and inspector_name != '':
            st.info(f"Выбрано для проверки {selected_product}")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM product_types WHERE name = ?", (selected_product,))
            prod_id = cursor.fetchone()[0]
            results = {}
            results = create_checklist(conn, [2], results)
            if st.button("Сохранить результат"):
                save_result(conn, 1, batch_number, prod_id, None, inspector_name, results)
                
        if form_of_control == "Операционный контроль (пошив)" and inspector_name != '':
            st.info(f"Выбрано для проверки {selected_product}")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM product_types WHERE name = ?", (selected_product,))
            prod_id = cursor.fetchone()[0]
            results = {}
            results = create_checklist(conn, [3], results)
            if st.button("Сохранить результат"):
                save_result(conn, 2, batch_number, prod_id, None, inspector_name, results)
                
        if form_of_control == "Приёмочный контроль" and inspector_name != '':
            st.info(f"Выбрано для проверки {selected_product}")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM product_types WHERE name = ?", (selected_product,))
            prod_id = cursor.fetchone()[0]
            cursor.execute("SELECT zipper FROM product_types WHERE name = ?", (selected_product,))
            zip = cursor.fetchone()[0]
            cursor.execute("SELECT button FROM product_types WHERE name = ?", (selected_product,))
            but = cursor.fetchone()[0]
            cursor.execute("SELECT velcro FROM product_types WHERE name = ?", (selected_product,))
            vel = cursor.fetchone()[0]
            cursor.execute("SELECT filler FROM product_types WHERE name = ?", (selected_product,))
            fil = cursor.fetchone()[0]
            
            required_form = []
            if zip == 1:
                required_form.append(4)
            if vel == 1:
                required_form.append(5)
            if but == 1:
                required_form.append(6)
            if fil == 1:
                required_form.append(7)
            required_form.append(8)
            results = {}
            results = create_checklist(conn, required_form, results)
            if st.button("Сохранить результат", type="primary"):
                save_result(conn, 3, batch_number, prod_id, None, inspector_name, results)
if menu == "Архив проверок":
    st.title("Архив проверок")
    archive_page(conn)
    
if menu == "Анализ качества":
    analysis_page(conn)
