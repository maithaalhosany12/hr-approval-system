import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# إعداد قاعدة البيانات (تأكدي أن database.py محدث أيضاً إذا لزم الأمر)
def init_db():
    conn = sqlite3.connect('requests.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  job_number TEXT, name TEXT, job_title TEXT, unit TEXT, appt_date TEXT,
                  subject_type TEXT, target_entity TEXT, transfer_reasons TEXT, 
                  notes TEXT, submit_date TIMESTAMP, signature TEXT, status TEXT, stage INTEGER)''')
    conn.commit()
    conn.close()

init_db()

st.title("📋 نظام الطلبات الإدارية المطور")

menu = ["تقديم طلب جديد", "متابعة حالة الطلب", "بوابة الاعتمادات"]
choice = st.sidebar.selectbox("القائمة الرئيسية", menu)

if choice == "تقديم طلب جديد":
    st.header("نموذج تقديم الطلب")
    
    # تقسيم العمل إلى خطوتين باستخدام Tabs
    tab1, tab2 = st.tabs(["👤 الخطوة 1: بيانات مقدم الطلب", "📝 الخطوة 2: تفاصيل موضوع الطلب"])

    with tab1:
        st.subheader("البيانات الأساسية")
        job_number = st.text_input("الرقم الوظيفي")
        full_name = st.text_input("الاسم الكامل")
        job_title = st.text_input("المسمى الوظيفي")
        unit = st.text_input("الوحدة / القسم")
        appt_date = st.date_input("تاريخ التعيين")
        st.info("💡 انتقل للخطوة التالية لتكملة بيانات الطلب")

    with tab2:
        st.subheader("تفاصيل الطلب")
        subject_type = st.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
        
        target_entity = ""
        transfer_reasons = ""
        if subject_type == "نقل":
            target_entity = st.text_input("الجهة المنقول إليها (وحدة معينة أو جهة أخرى)")
            transfer_reasons = st.text_area("أسباب النقل")
        
        notes = st.text_area("ملاحظات إضافية")
        
        # المرفقات تظهر فقط في حالات معينة
        if subject_type in ["تغيير مهنة", "إنهاء خدمة"]:
            attachment = st.file_uploader("يرجى إرفاق المستندات الداعمة")
        
        submit_date = st.date_input("تاريخ تقديم الطلب", datetime.now())
        signature = st.text_input("توقيع مقدم الطلب (اكتب اسمك الثلاثي كإقرار بالصحة)")

        if st.button("إرسال الطلب نهائياً"):
            if job_number and full_name and signature:
                conn = sqlite3.connect('requests.db')
                c = conn.cursor()
                c.execute("""INSERT INTO requests 
                          (job_number, name, job_title, unit, appt_date, subject_type, 
                           target_entity, transfer_reasons, notes, submit_date, signature, status, stage) 
                          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                          (job_number, full_name, job_title, unit, str(appt_date), subject_type,
                           target_entity, transfer_reasons, notes, str(submit_date), signature, "قيد التدقيق - المسؤول المباشر", 1))
                conn.commit()
                st.success(f"✅ تم إرسال طلبك بنجاح يا {full_name}")
                st.balloons()
            else:
                st.error("⚠️ يرجى التأكد من تعبئة الرقم الوظيفي، الاسم، والتوقيع.")

elif choice == "متابعة حالة الطلب":
    st.header("البحث عن طلب")
    search_id = st.number_input("أدخل رقم الطلب", step=1)
    if search_id:
        conn = sqlite3.connect('requests.db')
        df = pd.read_sql(f"SELECT * FROM requests WHERE id = {search_id}", conn)
        if not df.empty:
            st.write(f"**الحالة الحالية:** {df['status'].values[0]}")
            st.write(f"**المرحلة:** {df['stage'].values[0]} من 3")
            
            # حساب الأيام المتوقعة (افتراضي: كل مرحلة تأخذ يومين عمل)
            days_passed = (datetime.now() - datetime.strptime(df['submit_date'].values[0], '%Y-%m-%d')).days
            st.info(f"📅 مر على تقديم الطلب: {days_passed} يوم/أيام.")
            st.write("⏱️ **الوقت المتوقع للاعتماد:** يستغرق كل إجراء من 2-3 أيام عمل في كل مرحلة.")
        else:
            st.error("الطلب غير موجود")
