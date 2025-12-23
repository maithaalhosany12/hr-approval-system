import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# إعداد الصفحة وتنسيق CSS
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide")

# --- تنسيقات الواجهة لتشبه المنصات الاحترافية ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTabs [data-baseweb="tab-list"] { background-color: #ffffff; border-radius: 15px; padding: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .stTabs [data-baseweb="tab"] { font-weight: bold; color: #5d5fef; }
    .info-card { background-color: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border-right: 8px solid #5d5fef; margin-bottom: 25px; }
    div[data-testid="stExpander"] { border-radius: 15px; border: none; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

def init_db():
    conn = sqlite3.connect('requests.db')
    c = conn.cursor()
    # إذا تغيرت الأعمدة، سيتم تحديث الجدول
    try:
        c.execute("SELECT job_title FROM requests LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("DROP TABLE IF EXISTS requests")
    
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  job_number TEXT, name TEXT, job_title TEXT, unit TEXT, appt_date TEXT,
                  subject_type TEXT, target_entity TEXT, notes TEXT, 
                  submit_date TEXT, signature TEXT, status TEXT, stage INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# --- محتوى الموقع الرئيسي ---
st.markdown("<h1 style='text-align: right; color: #2d3436;'>📋 نظام الخدمات الذاتية للموظفين</h1>", unsafe_allow_html=True)

menu = ["تقديم طلب جديد", "متابعة الطلبات", "الاعتمادات الإدارية"]
choice = st.sidebar.radio("التنقل في النظام", menu)

if choice == "تقديم طلب جديد":
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["👤 بيانات الموظف", "📝 تفاصيل الطلب"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            job_number = st.text_input("الرقم الوظيفي")
            full_name = st.text_input("الاسم الثلاثي")
        with col2:
            job_title = st.text_input("المسمى الوظيفي")
            unit = st.text_input("الوحدة")
        appt_date = st.date_input("تاريخ التعيين")

    with tab2:
        subject_type = st.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
        
        # حقل النقل بدون أسباب كما طلبتِ
        target_entity = ""
        if subject_type == "نقل":
            target_entity = st.text_input("الجهة المطلوب النقل إليها")
        
        # المرفقات تظهر فقط في تغيير المهنة أو إنهاء الخدمة
        if subject_type in ["تغيير مهنة", "إنهاء خدمة"]:
            st.warning(f"مطلوب إرفاق مستندات لحالة: {subject_type}")
            st.file_uploader("رفع المستند")

        notes = st.text_area("ملاحظات إضافية")
        st.markdown("---")
        signature = st.text_input("التوقيع الرقمي (اكتب اسمك الثلاثي للإقرار بالبيانات)")

        if st.button("إرسال الطلب للاعتماد"):
            if job_number and full_name and signature:
                conn = sqlite3.connect('requests.db')
                c = conn.cursor()
                c.execute("""INSERT INTO requests 
                          (job_number, name, job_title, unit, appt_date, subject_type, 
                           target_entity, notes, submit_date, signature, status, stage) 
                          VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                          (job_number, full_name, job_title, unit, str(appt_date), subject_type,
                           target_entity, notes, datetime.now().strftime("%Y-%m-%d"), signature, "بانتظار المدير المباشر", 1))
                conn.commit()
                st.success("✅ تم استلام طلبك ورفعه للمراجعة")
                st.balloons()
            else:
                st.error("❗ يرجى استكمال كافة البيانات الأساسية")
    st.markdown('</div>', unsafe_allow_html=True)

elif choice == "متابعة الطلبات":
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    search_id = st.number_input("أدخل رقم المعاملة", step=1, value=0)
    if search_id > 0:
        conn = sqlite3.connect('requests.db')
        df = pd.read_sql(f"SELECT * FROM requests WHERE id = {search_id}", conn)
        if not df.empty:
            st.info(f"المرحلة الحالية: {df['status'].values[0]}")
            st.progress(int(df['stage'].values[0]) / 3)
            
            with st.expander("عرض تفاصيل المعاملة"):
                st.write(f"**الاسم:** {df['name'].values[0]}")
                st.write(f"**نوع الطلب:** {df['subject_type'].values[0]}")
                st.write(f"**تاريخ التقديم:** {df['submit_date'].values[0]}")
        else:
            st.error("رقم المعاملة غير موجود")
    st.markdown('</div>', unsafe_allow_html=True)
