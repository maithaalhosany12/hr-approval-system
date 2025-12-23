import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# إعداد الصفحة وتنسيق CSS لجعل الواجهة تشبه المنصات التعليمية
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #5d5fef; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: white; border-radius: 10px; padding: 10px 20px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .info-card {
        background-color: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-top: 5px solid #5d5fef;
        margin-bottom: 20px;
    }
    h1, h2, h3 { color: #2d3436; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# دالة إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect('requests.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  job_number TEXT, name TEXT, job_title TEXT, unit TEXT, appt_date TEXT,
                  subject_type TEXT, target_entity TEXT, notes TEXT, 
                  submit_date TIMESTAMP, signature TEXT, status TEXT, stage INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# العناوين العلوية
st.markdown("<h1 style='text-align: center;'>💻 نظام الطلبات الذكي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>أهلاً بك في منصة إدارة خدمات الموظفين</p>", unsafe_allow_html=True)

menu = ["تقديم طلب جديد", "متابعة حالة الطلب", "بوابة الاعتمادات"]
choice = st.sidebar.selectbox("القائمة الرئيسية", menu)

if choice == "تقديم طلب جديد":
    # تصميم الواجهة كبطاقة واحدة كبيرة
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["👤 أولاً: بيانات مقدم الطلب", "📝 ثانياً: موضوع الطلب"])

    with tab1:
        st.subheader("البيانات الشخصية والوظيفية")
        col1, col2 = st.columns(2)
        with col1:
            job_number = st.text_input("الرقم الوظيفي")
            full_name = st.text_input("الاسم الكامل")
        with col2:
            job_title = st.text_input("المسمى الوظيفي")
            unit = st.text_input("الوحدة / القسم")
        appt_date = st.date_input("تاريخ التعيين")

    with tab2:
        st.subheader("تحديد موضوع الطلب")
        subject_type = st.selectbox("اختر نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
        
        target_entity = ""
        if subject_type == "نقل":
            target_entity = st.text_input("الجهة المطلوب النقل إليها (وحدة أو جهة معينة)")
            # تم حذف أسباب النقل بناءً على طلبك
        
        notes = st.text_area("ملاحظات إضافية (اختياري)")
        
        if subject_type in ["تغيير مهنة", "إنهاء خدمة"]:
            st.info(f"يرجى إرفاق المستندات الخاصة بحالة {subject_type}")
            attachment = st.file_uploader("رفع المرفق")
        
        st.markdown("---")
        signature = st.text_input("إقرار بصحة البيانات: اكتب اسمك الثلاثي كـ (توقيع رقمي)")

        if st.button("اعتماد وإرسال الطلب"):
            if job_number and full_name and signature:
                conn = sqlite3.connect('requests.db')
                c = conn.cursor()
                c.execute("""INSERT INTO requests 
                          (job_number, name, job_title, unit, appt_date, subject_type, 
                           target_entity, notes, submit_date, signature, status, stage) 
                          VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                          (job_number, full_name, job_title, unit, str(appt_date), subject_type,
                           target_entity, notes, datetime.now().strftime("%Y-%m-%d"), signature, "بانتظار موافقة المسؤول المباشر", 1))
                conn.commit()
                st.success("تم إرسال الطلب بنجاح وهو الآن تحت الإجراء")
            else:
                st.warning("الرجاء إكمال جميع البيانات الأساسية والتوقيع")
    st.markdown('</div>', unsafe_allow_html=True)

elif choice == "متابعة حالة الطلب":
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    search_id = st.number_input("أدخل رقم الطلب للمتابعة", step=1, value=0)
    if search_id > 0:
        conn = sqlite3.connect('requests.db')
        df = pd.read_sql(f"SELECT * FROM requests WHERE id = {search_id}", conn)
        if not df.empty:
            st.success(f"حالة الطلب: {df['status'].values[0]}")
            
            # عرض عداد زمني بسيط
            submit_dt = datetime.strptime(df['submit_date'].values[0], "%Y-%m-%d")
            days_elapsed = (datetime.now() - submit_dt).days
            
            st.write(f"⏱️ تاريخ التقديم: {df['submit_date'].values[0]}")
            st.write(f"⏱️ مدة الطلب الحالية: {days_elapsed} أيام")
            
            # خط تقدم (Progress Bar) بناءً على المرحلة
            stage = df['stage'].values[0]
            progress = (stage / 3)
            st.progress(progress)
            st.write(f"المرحلة الحالية: {stage} من 3 (الاعتماد النهائي عند المرحلة 3)")
        else:
            st.error("رقم الطلب غير صحيح")
    st.markdown('</div>', unsafe_allow_html=True)
