import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import time
import random

# --- 1. وظائف قاعدة البيانات ---
def init_db():
    conn = sqlite3.connect('hr_system.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests 
                 (order_id TEXT PRIMARY KEY, emp_id TEXT, name TEXT, title TEXT, 
                  dept TEXT, hire_date TEXT, req_type TEXT, status TEXT, 
                  stage INTEGER, created_at TEXT, stage_start TEXT, notes TEXT)''')
    conn.commit()
    return conn

def add_request_to_db(data):
    conn = init_db()
    c = conn.cursor()
    c.execute("INSERT INTO requests VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", data)
    conn.commit()

def update_request_status(order_id, new_stage, new_status):
    conn = init_db()
    c = conn.cursor()
    c.execute("UPDATE requests SET stage=?, status=?, stage_start=? WHERE order_id=?", 
              (new_stage, new_status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), order_id))
    conn.commit()

# --- 2. إعداد الصفحة والتنسيق (الأصلي) ---
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main { direction: rtl !important; text-align: right !important; background-color: #f4f7f9; }
    .block-container { max-width: 1100px !important; padding-top: 1.5rem; }
    .company-header {
        display: flex; align-items: center; justify-content: flex-start;
        padding: 15px 25px; background: white; border-radius: 15px; margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-right: 6px solid #5d5fef;
    }
    .header-logo img { width: 45px; margin-left: 15px; }
    .header-text h1 { margin: 0; font-size: 19px; color: #2d3436; font-weight: bold; }
    .step-block { position: relative; padding-right: 60px; margin-bottom: 30px; }
    .step-icon {
        position: absolute; right: 8px; top: 0;
        width: 42px; height: 42px; border-radius: 50%;
        background-color: #5d5fef; color: white;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; z-index: 3; font-size: 18px;
    }
    .content-box { background-color: white; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.04); overflow: hidden; border: 1px solid #eef0f2; }
    .step-header { background: linear-gradient(90deg, #5d5fef, #7a7cfc); color: white; padding: 12px 25px; font-size: 15px; font-weight: bold; }
    .form-body { padding: 20px 25px; }
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input { min-height: 32px !important; height: 32px !important; text-align: right !important; border-radius: 8px !important; }
    .stat-card { background: white; padding: 15px; border-radius: 10px; border-top: 4px solid #5d5fef; box-shadow: 0 2px 5px rgba(0,0,0,0.05); text-align: center; }
    .approval-card { background: #ffffff; border: 1px solid #e2e8f0; padding: 15px; border-radius: 12px; margin-bottom: 10px; }
    .active-card { border-right: 5px solid #5d5fef; background: #f8faff; }
    .locked-card { background: #f1f5f9; opacity: 0.6; pointer-events: none; }
    .notification-timer { background-color: #fff4f4; border: 1px solid #ffcdd2; color: #c62828; padding: 12px; border-radius: 10px; font-weight: bold; margin-bottom: 15px; text-align: center; border-right: 5px solid #c62828; }
    .styled-table { width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; }
    .styled-table th, .styled-table td { padding: 12px 15px; border-bottom: 1px solid #eee; text-align: right; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة الحالة ---
if 'order_id' not in st.session_state: st.session_state.order_id = f"REQ-{random.randint(1000, 9999)}"

st.markdown('<div class="company-header"><div class="header-logo"><img src="https://cdn-icons-png.flaticon.com/512/281/281764.png"></div><div class="header-text"><h1>مؤسسة المسار المتكامل</h1><p>نظام الرقابة والطلبات الموحد</p></div></div>', unsafe_allow_html=True)

with st.sidebar:
    st.title("⚙️ القائمة الرئيسية")
    choice = st.selectbox("انتقل إلى:", ["تقديم طلب جديد", "متابعة الطلبات", "الاعتمادات"])

# --- الصفحة 1: تقديم الطلب ---
if choice == "تقديم طلب جديد":
    st.markdown('<div class="step-block"><div class="step-icon">1</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">👤 الخطوة الأولى: بيانات مقدم الطلب</div><div class="form-body">', unsafe_allow_html=True)
        r_col, _ = st.columns([1, 4])
        with r_col: st.text_input("رقم الطلب", value=st.session_state.order_id, disabled=True)
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: emp_id = st.text_input("الرقم الوظيفي")
        with c2: name = st.text_input("الاسم الكامل")
        with c3: title = st.text_input("المسمى")
        with c4: dept = st.text_input("القسم")
        with c5: hire_date = st.date_input("تاريخ التعيين")
        st.markdown('</div></div></div>', unsafe_allow_html=True)

    st.markdown('<div class="step-block"><div class="step-icon">2</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">📝 الخطوة الثانية: تفاصيل الطلب</div><div class="form-body">', unsafe_allow_html=True)
        cx, cy = st.columns(2)
        with cx: req_type = st.selectbox("نوع الطلب", ["نقل داخلي", "تعديل مهنة", "إنهاء خدمة"])
        with cy: st.date_input("تاريخ السريان", value=datetime.now(), disabled=True)
        st.text_area("ملاحظات إضافية تفصيلية", height=100)
        col_btn, _ = st.columns([1, 3])
        if col_btn.button("إرسال الطلب الآن", use_container_width=True):
            if emp_id and name:
                data = (st.session_state.order_id, emp_id, name, title, dept, str(hire_date), 
                        req_type, "بانتظار الاعتماد", 1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "")
                add_request_to_db(data)
                st.success("تم الحفظ بنجاح!")
                st.session_state.order_id = f"REQ-{random.randint(1000, 9999)}"
            else: st.error("يرجى ملء البيانات")
        st.markdown('</div></div></div>', unsafe_allow_html=True)

# --- الصفحة 2: متابعة الطلبات ---
elif choice == "متابعة الطلبات":
    st.markdown("### 🔍 سجل الطلبات")
    conn = init_db()
    df = pd.read_sql_query("SELECT order_id, name, req_type, status, created_at FROM requests", conn)
    st.table(df)

# --- الصفحة 3: الاعتمادات (إضافة الخانات المطلوبة) ---
elif choice == "الاعتمادات":
    conn = init_db()
    pending_df = pd.read_sql_query("SELECT * FROM requests WHERE status != 'مكتمل'", conn)
    if pending_df.empty: st.write("لا توجد طلبات معلقة.")
    else:
        selected_id = st.selectbox("اختر الطلب للمراجعة:", pending_df['order_id'])
        req = pending_df[pending_df['order_id'] == selected_id].iloc[0]
        
        start_dt = datetime.strptime(req['stage_start'], '%Y-%m-%d %H:%M:%S')
        remaining = 45 - (datetime.now() - start_dt).days
        st.markdown(f'<div class="notification-timer">المتبقي لاتخاذ القرار: {remaining} يوم</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        stages = ["المدير المباشر", "HR", "المدير العام"]
        for i, stage_name in enumerate(stages, 1):
            with [col1, col2, col3][i-1]:
                active = (req['stage'] == i)
                st.markdown(f'<div class="approval-card {"active-card" if active else "locked-card"}"><b>{stage_name}</b></div>', unsafe_allow_html=True)
                
                # الخانات الجديدة المضافة
                st.text_input("المنصب", key=f"pos_{i}", disabled=not active)
                st.text_input("الوظيفة", key=f"job_{i}", disabled=not active)
                st.date_input("التاريخ", key=f"date_{i}", disabled=not active)
                st.file_uploader("التوقيع", key=f"sig_{i}", disabled=not active)
                
                res = st.selectbox("القرار", ["قيد الانتظار", "موافق", "مرفوض"], key=f"res_{i}", disabled=not active)
                reason = st.text_area("المبررات", key=f"rea_{i}", disabled=not active)
                
                if active and st.button(f"حفظ قرار {stage_name}"):
                    if reason:
                        new_stage = i + 1 if res == "موافق" and i < 3 else i
                        new_status = "مكتمل" if res == "موافق" and i == 3 else "مرفوض" if res == "مرفوض" else "بانتظار المرحلة التالية"
                        update_request_status(selected_id, new_stage, new_status)
                        st.success("تم الاعتماد")
                        st.rerun()
                    else: st.warning("المبررات مطلوبة")
