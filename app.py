import streamlit as st
from datetime import datetime
import time

# 1. إعداد الصفحة
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="collapsed")

# 2. تنسيق CSS (نفس التصميم الفخم المعتمد)
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
    .step-block::before {
        content: ""; position: absolute; right: 28px; top: 45px; bottom: -45px;
        width: 3px; background-color: #5d5fef; z-index: 1; opacity: 0.2;
    }
    .step-block:last-child::before { display: none; }
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
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input { min-height: 32px !important; height: 32px !important; text-align: right !important; font-size: 13px !important; border-radius: 8px !important; }
    label { font-size: 12px !important; font-weight: bold !important; margin-bottom: 4px !important; color: #475569 !important;}
    .styled-table { width: 100%; border-collapse: collapse; margin-top: 10px; background: white; border-radius: 10px; overflow: hidden; }
    .styled-table thead tr { background-color: #5d5fef; color: white; text-align: right; }
    .styled-table th, .styled-table td { padding: 12px 15px; border-bottom: 1px solid #eee; font-size: 13px; }
    .status-badge { padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; }
    .status-pending { background: #fff3cd; color: #856404; }
    .status-done { background: #d4edda; color: #155724; }
    </style>
    """, unsafe_allow_html=True)

# إدارة حالة الصفحة لضمان الانتقال
if 'page' not in st.session_state:
    st.session_state.page = 'form'

# 3. الهيدر
st.markdown("""
    <div class="company-header">
        <div class="header-logo"><img src="https://cdn-icons-png.flaticon.com/512/281/281764.png"></div>
        <div class="header-text">
            <h1>مؤسسة المسار المتكامل</h1>
            <p>قسم الموارد البشرية - نموذج الطلبات الإلكتروني</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# القائمة الجانبية (تحديث الحالة عند الاختيار)
with st.sidebar:
    st.title("القائمة")
    menu_choice = st.radio("اختر الوجهة:", ["تقديم طلب جديد", "متابعة الطلبات"], label_visibility="collapsed")
    if menu_choice == "متابعة الطلبات":
        st.session_state.page = 'tracking'
    else:
        st.session_state.page = 'form'

# --- صفحة النموذج ---
if st.session_state.page == 'form':
    
    st.markdown('<div class="step-block"><div class="step-icon">1</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">👤 الخطوة الأولى: بيانات مقدم الطلب</div><div class="form-body">', unsafe_allow_html=True)
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.text_input("الرقم الوظيفي", key="job_id")
        with c2: st.text_input("الاسم الكامل", key="full_name")
        with c3: st.text_input("المسمى", key="title")
        with c4: st.text_input("القسم", key="dept")
        with c5: st.date_input("تاريخ التعيين", key="hire_date")
        st.markdown('</div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="step-block"><div class="step-icon">2</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">📝 الخطوة الثانية: تفاصيل الطلب</div><div class="form-body">', unsafe_allow_html=True)
        c6, c7, c8 = st.columns([1, 1, 2])
        with c6: req_type = st.selectbox("نوع الطلب", ["نقل داخلي", "تعديل مهنة", "إنهاء خدمة"], key="req_type")
        with c7: st.date_input("تاريخ السريان", value=datetime.now(), disabled=True)
        with c8: st.text_input("ملاحظات إضافية", key="notes")
        
        if req_type in ["تعديل مهنة", "إنهاء خدمة"]:
            st.markdown("<div style='margin-top:10px; color:#5d5fef; font-size:13px;'>📎 يرجى إرفاق المستندات الداعمة</div>", unsafe_allow_html=True)
            st.file_uploader("تحميل المرفقات", type=['pdf', 'png', 'jpg'], key="attach", label_visibility="collapsed")

        st.markdown("<div style='margin-top:15px;'><b>✍️ التوقيع الرقمي</b></div>", unsafe_allow_html=True)
        c9, c10 = st.columns([3, 1])
        with c9: st.file_uploader("توقيعك", type=['png', 'jpg'], key="sig", label_visibility="collapsed")
        with c10: 
            st.markdown("<div style='height:0px;'></div>", unsafe_allow_html=True)
            submit_btn = st.button("إرسال الطلب", use_container_width=True)
        
        if submit_btn:
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # رسالة نجاح واضحة جداً
            st.success("🎉 تم إرسال طلبك بنجاح! جاري تحويلك الآن...")
            
            # تحديث الحالة البرمجية فوراً قبل الـ sleep
            st.session_state.page = 'tracking'
            
            time.sleep(2)
            st.rerun() # إعادة التشغيل ستأخذ المستخدم لصفحة tracking بناءً على الحالة الجديدة

        st.markdown('</div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التتبع ---
elif st.session_state.page == 'tracking':
    st.markdown("<h3 style='text-align:right;'>🔍 سجل الطلبات والمتابعة</h3>", unsafe_allow_html=True)
    
    table_html = """
    <table class="styled-table">
        <thead>
            <tr><th>رقم الطلب</th><th>نوع الطلب</th><th>تاريخ التقديم</th><th>المرفقات</th><th>الحالة</th></tr>
        </thead>
        <tbody>
            <tr><td>#1028</td><td>تعديل مهنة</td><td>2023-12-20</td><td>موجود 📎</td><td><span class="status-badge status-pending">قيد الاعتماد</span></td></tr>
            <tr><td>#1025</td><td>إنهاء خدمة</td><td>2023-11-15</td><td>موجود 📎</td><td><span class="status-badge status-pending">تحت المراجعة</span></td></tr>
            <tr><td>#1024</td><td>نقل داخلي</td><td>2023-10-01</td><td>-</td><td><span class="status-badge status-done">مكتمل</span></td></tr>
        </tbody>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)
    
    if st.button("العودة لتقديم طلب جديد"):
        st.session_state.page = 'form'
        st.rerun()
