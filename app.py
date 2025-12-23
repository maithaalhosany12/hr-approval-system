import streamlit as st
import sqlite3
from datetime import datetime
import time

# 1. إعداد الصفحة وتصغير التصميم (Compact Design)
st.set_page_config(page_title="نظام الطلبات الإدارية", layout="wide", initial_sidebar_state="collapsed")

# تنسيق CSS مخصص لتلبية طلباتك (إلغاء السكرول، تصغير الحقول، التايم لاين)
st.markdown("""
    <style>
    /* تصغير الحقول والمسافات */
    .stTextInput>div>div>input, .stSelectbox>div>div>div { padding: 5px 10px; min-height: 30px; border-radius: 8px; }
    .stDateInput>div>div>input { min-height: 30px; border-radius: 8px; }
    div[data-testid="stExpander"] { border: none; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 10px; }
    
    /* هيدر الشركة */
    .company-header {
        display: flex; align-items: center; justify-content: space-between;
        padding: 15px 25px; background: white; border-radius: 12px; margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); border-right: 5px solid #5d5fef;
    }

    /* الـ Timeline الاحترافي */
    .timeline-container {
        display: flex; justify-content: space-around; align-items: flex-start;
        background: white; padding: 25px; border-radius: 15px; margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .step-item { text-align: center; position: relative; flex: 1; }
    .step-dot { 
        width: 30px; height: 30px; background: #e0e0e0; border-radius: 50%; 
        margin: 0 auto 10px; display: flex; align-items: center; justify-content: center;
        color: white; font-weight: bold; font-size: 14px;
    }
    .step-item.active .step-dot { background: #5d5fef; box-shadow: 0 0 10px rgba(93,95,239,0.5); }
    .step-label { font-size: 14px; color: #333; font-weight: 500; }
    .step-status { font-size: 11px; color: #888; }
    </style>
    """, unsafe_allow_html=True)

# إدارة حالة الصفحة (Navigation Logic)
if 'page' not in st.session_state:
    st.session_state.page = 'form'

# دالة تهيئة قاعدة البيانات المحلية (SQLite)
def init_db():
    conn = sqlite3.connect('requests.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  job_number TEXT, name TEXT, job_title TEXT, unit TEXT, 
                  subject_type TEXT, subject_date TEXT, notes TEXT, 
                  signature_path TEXT, status TEXT, stage INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# 5. أيقونة الشركة + نص القسم (Header)
st.markdown("""
    <div class="company-header">
        <div style="display: flex; align-items: center;">
            <div style="background: #5d5fef; padding: 8px; border-radius: 8px; margin-left: 15px;">
                <img src="https://cdn-icons-png.flaticon.com/512/281/281764.png" width="30" style="filter: brightness(0) invert(1);">
            </div>
            <div>
                <div style="font-weight: bold; font-size: 18px; color: #2d3436;">مؤسسة الرؤية الرقمية</div>
                <div style="font-size: 13px; color: #636e72;">نظام إدارة شؤون الموظفين الموحد</div>
            </div>
        </div>
        <div style="text-align: left;">
            <div style="font-weight: 600; color: #5d5fef;">قسم الموارد البشرية</div>
            <div style="font-size: 11px; color: #b2bec3;">تاريخ اليوم: """ + datetime.now().strftime('%Y-%m-%d') + """</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# الشريط الجانبي (Drop-down فقط بدون عناوين)
with st.sidebar:
    choice = st.selectbox("", ["تقديم طلب جديد", "متابعة الطلبات"], label_visibility="collapsed")
    if choice == "متابعة الطلبات":
        st.session_state.page = 'tracking'

# --- الصفحة الأولى: نموذج تقديم الطلب ---
if st.session_state.page == 'form':
    st.markdown("<h4 style='margin-bottom:20px;'>📝 إنشاء طلب إداري جديد</h4>", unsafe_allow_html=True)
    
    # استخدام حاوية لتقليل العرض وجعلها Compact
    col_content = st.columns([1, 8, 1])[1]
    
    with col_content:
        # الخطوة 1: بيانات الموظف
        with st.expander("👤 1. بيانات مقدم الطلب", expanded=True):
            c1, c2 = st.columns(2)
            job_num = c1.text_input("الرقم الوظيفي")
            full_name = c2.text_input("الاسم الكامل")
            job_title = c1.text_input("المسمى الوظيفي")
            unit = c2.text_input("الوحدة / القسم")
        
        # الخطوة 2: تفاصيل الطلب
        with st.expander("📄 2. تفاصيل موضوع الطلب والاعتماد", expanded=True):
            c3, c4 = st.columns(2)
            sub_type = c3.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
            # 1. تاريخ السريان أوتوماتيك
            sub_date = c4.date_input("تاريخ سريان الطلب", value=datetime.now(), disabled=True)
            
            notes = st.text_area("ملاحظات إضافية", height=60)
            
            st.markdown("<div style='margin-top:10px; font-weight:bold; font-size:14px;'>✍️ التوقيع الرقمي (صورة)</div>", unsafe_allow_html=True)
            # 2. التوقيع الرقمي كصورة
            sig_file = st.file_uploader("اسحب صورة توقيعك هنا أو اختر ملف", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

        # زر الإرسال
        if st.button("إرسال الطلب للاعتماد النهائي"):
            if job_num and full_name and sig_file:
                # 3. إظهار Pop-up نجاح (Toast)
                st.toast("✅ جاري إرسال الطلب وحفظ البيانات...", icon="📩")
                time.sleep(1.5)
                
                # حفظ البيانات في SQLite (محاكاة)
                st.toast("🚀 تم الإرسال بنجاح! يتم الآن تحويلك...", icon="🎉")
                
                # 7. تحويل أوتوماتيك لصفحة الطلبات
                st.session_state.page = 'tracking'
                st.rerun()
            else:
                st.error("⚠️ يرجى التأكد من إدخال كافة البيانات ورفع صورة التوقيع.")

# --- الصفحة الثانية: متابعة الطلبات والـ Timeline ---
elif st.session_state.page == 'tracking':
    st.markdown("<h4 style='margin-bottom:10px;'>🔍 تتبع حالة معاملاتك</h4>", unsafe_allow_html=True)
    
    # 4. التايم لاين للطلب الأخير
    st.markdown("""
        <div class="timeline-container">
            <div class="step-item active">
                <div class="step-dot">1</div>
                <div class="step-label">تقديم الطلب</div>
                <div class="step-status">مكتمل</div>
            </div>
            <div class="step-item active">
                <div class="step-dot">2</div>
                <div class="step-label">مراجعة HR</div>
                <div class="step-status">قيد المعالجة</div>
            </div>
            <div class="step-item">
                <div class="step-dot">3</div>
                <div class="step-label">اعتماد المدير</div>
                <div class="step-status">بانتظار</div>
            </div>
            <div class="step-item">
                <div class="step-dot">4</div>
                <div class="step-label">الأرشفة</div>
                <div class="step-status">---</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    

    st.success("حالة الطلب: تم استلام طلبك وهو الآن في مرحلة **المراجعة الفنية** لدى قسم الموارد البشرية.")
    
    if st.button("⬅️ العودة لتقديم طلب جديد"):
        st.session_state.page = 'form'
        st.rerun()
