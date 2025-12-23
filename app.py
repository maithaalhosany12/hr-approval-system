import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# إعداد الصفحة وتنسيق الواجهة
st.set_page_config(page_title="نظام شؤون الموظفين", layout="centered")

# تنسيق CSS مخصص للأرقام والبطاقات لضمان مظهر الـ Scrolling المرتب
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    
    /* تنسيق الدائرة الرقمية لتكون ملاصقة للعنوان */
    .step-number {
        display: inline-block;
        width: 35px; height: 35px; border-radius: 50%;
        background-color: #5d5fef; color: white;
        text-align: center; line-height: 35px;
        font-weight: bold; margin-left: 15px;
        box-shadow: 0 2px 5px rgba(93, 95, 239, 0.3);
    }
    
    /* تنسيق بطاقات الأقسام (Scrolling Cards) */
    .main-card {
        background-color: white; padding: 35px; border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-bottom: 30px;
        border-right: 6px solid #5d5fef;
    }
    
    .section-title {
        display: flex; align-items: center;
        margin-bottom: 25px; color: #2d3436;
        font-size: 20px; font-weight: bold;
    }
    
    .stButton>button { 
        background-color: #5d5fef; color: white; 
        width: 100%; border-radius: 12px; height: 3.5em;
        font-size: 18px; font-weight: bold;
        transition: 0.3s; margin-top: 20px;
    }
    .stButton>button:hover { background-color: #4a4cd9; border: none; }
    
    hr { border: 0.5px solid #f0f2f6; margin: 25px 0; }
    </style>
    """, unsafe_allow_html=True)

# دالة ذكية لتهيئة قاعدة البيانات وحل مشاكل الأعمدة المفقودة تلقائياً
def init_db():
    conn = sqlite3.connect('requests.db')
    c = conn.cursor()
    try:
        # فحص وجود الأعمدة الحديثة لضمان عدم تعطل النظام
        c.execute("SELECT subject_date FROM requests LIMIT 1")
    except sqlite3.OperationalError:
        # في حال وجود تعارض مع النسخ القديمة، يتم إعادة بناء الجدول
        c.execute("DROP TABLE IF EXISTS requests")
    
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  job_number TEXT, name TEXT, job_title TEXT, unit TEXT, appt_date TEXT,
                  subject_type TEXT, subject_date TEXT, target_entity TEXT, notes TEXT, 
                  submit_date TEXT, signature TEXT, status TEXT, stage INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# القائمة الجانبية (Sidebar) للتنقل بين الأقسام
st.sidebar.markdown("### ⚙️ التنقل في النظام")
choice = st.sidebar.radio("", ["تقديم طلب جديد", "متابعة الطلبات", "الاعتمادات الإدارية"])

if choice == "تقديم طلب جديد":
    st.markdown("<h1 style='text-align: center; color: #2d3436;'>📝 نموذج تقديم طلب إداري</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- الخطوة الأولى: بيانات مقدم الطلب (Scrolling Card 1) ---
    st.markdown(f'''
        <div class="main-card">
            <div class="section-title">
                <span class="step-number">1</span> بيانات مقدم الطلب
            </div>
    ''', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        job_number = st.text_input("الرقم الوظيفي")
        full_name = st.text_input("الاسم الكامل")
    with col2:
        job_title = st.text_input("المسمى الوظيفي")
        unit = st.text_input("الوحدة / القسم")
    appt_date = st.date_input("تاريخ التعيين", key="appt")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- الخطوة الثانية: تفاصيل الطلب + الاعتماد (Scrolling Card 2) ---
    st.markdown(f'''
        <div class="main-card">
            <div class="section-title">
                <span class="step-number">2</span> تفاصيل موضوع الطلب والاعتماد
            </div>
    ''', unsafe_allow_html=True)
    
    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        subject_type = st.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
    with col_sub2:
        subject_date = st.date_input("تاريخ سريان الطلب", key="subj_date")
    
    if subject_type == "نقل":
        target_entity = st.text_input("الجهة المطلوب النقل إليها")
    else:
        target_entity = ""
        
    if subject_type in ["تغيير مهنة", "إنهاء خدمة"]:
        st.warning(f"💡 يرجى إرفاق المستندات الرسمية الداعمة لحالة: {subject_type}")
        st.file_uploader("تحميل المرفق")
        
    notes = st.text_area("ملاحظات إضافية")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<b>✍️ الإقرار والتوقيع الرقمي:</b>", unsafe_allow_html=True)
    signature = st.text_input("اكتب اسمك الثلاثي كإقرار بصحة البيانات")
    
    # زر الإرسال في نهاية التمرير
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
            st.success("✅ تم إرسال طلبك بنجاح. يمكنك متابعة الحالة برقم المعاملة.")
            st.balloons()
        else:
            st.error("⚠️ يرجى التأكد من تعبئة كافة البيانات الأساسية والتوقيع.")
    st.markdown('</div>', unsafe_allow_html=True)

elif choice == "متابعة الطلبات":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.header("🔍 استعلام عن حالة المعاملة")
    search_id = st.number_input("رقم المعاملة", step=1, value=0)
    if search_id > 0:
        conn = sqlite3.connect('requests.db')
        df = pd.read_sql(f"SELECT * FROM requests WHERE id = {search_id}", conn)
        if not df.empty:
            st.markdown(f"### الحالة الحالية: `{df['status'].values[0]}`")
            st.progress(int(df['stage'].values[0]) / 3)
            st.write(f"تاريخ التقديم: {df['submit_date'].values[0]}")
        else:
            st.error("رقم المعاملة غير موجود.")
    st.markdown('</div>', unsafe_allow_html=True)
