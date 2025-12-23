import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# إعداد الصفحة وتنسيق CSS لتصميم الـ Vertical Stepper
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide")

st.markdown("""
    <style>
    /* تنسيق الحاوية الرئيسية */
    .main { background-color: #f8f9fa; }
    
    /* تصميم الخطوات الجانبية (Stepper) */
    .stepper-container {
        position: sticky;
        top: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .step-circle {
        width: 45px; height: 45px; border-radius: 50%;
        background-color: #5d5fef; color: white;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 18px;
        box-shadow: 0 4px 10px rgba(93, 95, 239, 0.3);
        z-index: 2;
    }
    .step-line {
        width: 2px; height: 350px; /* طول الخط بين الدوائر */
        background-color: #5d5fef;
        margin-top: -5px; margin-bottom: -5px;
        z-index: 1;
    }
    
    /* تنسيق بطاقات المحتوى */
    .content-card {
        background-color: white; padding: 35px; border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-bottom: 40px;
        border-right: 5px solid #5d5fef;
    }
    h2 { color: #2d3436; font-size: 22px; margin-bottom: 25px; }
    
    /* تنسيق زر الإرسال */
    .stButton>button { 
        background-color: #5d5fef; color: white; 
        width: 100%; border-radius: 10px; height: 3.5em; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# دالة تهيئة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('requests.db')
    c = conn.cursor()
    try:
        c.execute("SELECT subject_date FROM requests LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("DROP TABLE IF EXISTS requests")
    
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  job_number TEXT, name TEXT, job_title TEXT, unit TEXT, appt_date TEXT,
                  subject_type TEXT, subject_date TEXT, target_entity TEXT, notes TEXT, 
                  submit_date TEXT, signature TEXT, status TEXT, stage INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# القائمة الجانبية (Sidebar)
choice = st.sidebar.radio("التنقل في النظام", ["تقديم طلب جديد", "متابعة الطلبات", "الاعتمادات الإدارية"])

if choice == "تقديم طلب جديد":
    st.markdown("<h1 style='text-align: center;'>📝 نموذج تقديم طلب جديد</h1><br>", unsafe_allow_html=True)

    # تقسيم الصفحة: عمود صغير للـ Stepper وعمود كبير للمحتوى
    col_stepper, col_content = st.columns([1, 6])

    with col_stepper:
        st.markdown('<div class="stepper-container">', unsafe_allow_html=True)
        st.markdown('<div class="step-circle">1</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-line"></div>', unsafe_allow_html=True)
        st.markdown('<div class="step-circle">2</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_content:
        # --- الخطوة 1: بيانات مقدم الطلب ---
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("<h2>👤 الخطوة الأولى: بيانات مقدم الطلب</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            job_number = st.text_input("الرقم الوظيفي")
            full_name = st.text_input("الاسم الكامل")
        with c2:
            job_title = st.text_input("المسمى الوظيفي")
            unit = st.text_input("الوحدة / القسم")
        appt_date = st.date_input("تاريخ التعيين", key="appt")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- الخطوة 2: تفاصيل الطلب + الاعتماد والتوقيع ---
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("<h2>📝 الخطوة الثانية: تفاصيل الطلب والاعتماد</h2>", unsafe_allow_html=True)
        
        cs1, cs2 = st.columns(2)
        with cs1:
            subject_type = st.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
        with cs2:
            subject_date = st.date_input("تاريخ سريان الطلب", key="subj_date")
        
        if subject_type == "نقل":
            target_entity = st.text_input("الجهة المطلوب النقل إليها")
        else:
            target_entity = ""
            
        if subject_type in ["تغيير مهنة", "إنهاء خدمة"]:
            st.info(f"يرجى إرفاق المستندات الخاصة بحالة: {subject_type}")
            st.file_uploader("تحميل المرفق الرسمي")
            
        notes = st.text_area("ملاحظات إضافية")
        
        st.markdown("<hr style='border: 0.5px solid #eee;'>", unsafe_allow_html=True)
        st.markdown("<b>✍️ الإقرار والتوقيع الرقمي:</b>", unsafe_allow_html=True)
        signature = st.text_input("اكتب اسمك الثلاثي كإقرار بصحة البيانات")
        
        if st.button("إرسال الطلب للاعتماد النهائي"):
            if job_number and full_name and signature:
                conn = sqlite3.connect('requests.db')
                c = conn.cursor()
                c.execute("""INSERT INTO requests 
                          (job_number, name, job_title, unit, appt_date, subject_type, subject_date,
                           target_entity, notes, submit_date, signature, status, stage) 
                          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                          (job_number, full_name, job_title, unit, str(appt_date), subject_type, str(subject_date),
                           target_entity, notes, datetime.now().strftime("%Y-%m-%d"), signature, "بانتظار موافقة المسؤول", 1))
                conn.commit()
                st.success("✅ تم إرسال الطلب بنجاح!")
                st.balloons()
            else:
                st.error("⚠️ يرجى استكمال البيانات والتوقيع.")
        st.markdown('</div>', unsafe_allow_html=True)

elif choice == "متابعة الطلبات":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.header("🔍 متابعة حالة الطلب")
    # ... كود المتابعة ...
    st.markdown('</div>', unsafe_allow_html=True)
