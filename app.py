import streamlit as st
from datetime import datetime
import time

# 1. إعداد الصفحة والتنسيق (ثابت تماماً كما هو)
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

    /* تنسيق المدخلات */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input { min-height: 32px !important; height: 32px !important; text-align: right !important; border-radius: 8px !important; }
    /* تنسيق خاص للملاحظات الكبيرة */
    .stTextArea>div>div>textarea { border-radius: 8px !important; text-align: right !important; font-size: 14px !important; }
    label { font-size: 12px !important; font-weight: bold !important; color: #475569 !important;}

    .styled-table { width: 100%; border-collapse: collapse; margin-top: 10px; background: white; border-radius: 10px; overflow: hidden; }
    .styled-table thead tr { background-color: #5d5fef; color: white; text-align: right; }
    .styled-table th, .styled-table td { padding: 12px 15px; border-bottom: 1px solid #eee; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# إدارة الحالة
if 'page' not in st.session_state:
    st.session_state.page = 'form'

# 3. الهيدر الرسمي
st.markdown("""
    <div class="company-header">
        <div class="header-logo"><img src="https://static.alittihad.ae/front/Content/Alittihad/img/logo-desktop.svg"></div>
        <div class="header-text">
            <h1>مؤسسة المسار المتكامل</h1>
            <p>قسم الموارد البشرية - نموذج الطلبات الإلكتروني</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# القائمة الجانبية (Dropdown)
with st.sidebar:
    st.title("⚙️ الإجراءات")
    choice = st.selectbox("انتقل إلى:", ["تقديم طلب جديد", "متابعة الطلبات", "الاعتمادات"], key="nav_menu")
    if choice == "تقديم طلب جديد": st.session_state.page = 'form'
    elif choice == "متابعة الطلبات": st.session_state.page = 'tracking'
    else: st.session_state.page = 'approvals'

# --- 1. صفحة النموذج ---
if st.session_state.page == 'form':
    # الخطوة 1: بيانات الموظف
    st.markdown('<div class="step-block"><div class="step-icon">1</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">👤 الخطوة الأولى: بيانات مقدم الطلب</div><div class="form-body">', unsafe_allow_html=True)
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.text_input("الرقم الوظيفي")
        with c2: st.text_input("الاسم الكامل")
        with c3: st.text_input("المسمى")
        with c4: st.text_input("القسم")
        with c5: st.date_input("تاريخ التعيين")
        st.markdown('</div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # الخطوة 2: تفاصيل الطلب والملاحظات
    st.markdown('<div class="step-block"><div class="step-icon">2</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">📝 الخطوة الثانية: تفاصيل الطلب</div><div class="form-body">', unsafe_allow_html=True)
        
        # النوع والتاريخ في سطر واحد
        c6, c7 = st.columns([1, 1])
        with c6: req_type = st.selectbox("نوع الطلب", ["نقل داخلي", "تعديل مهنة", "إنهاء خدمة"])
        with c7: st.date_input("تاريخ السريان", value=datetime.now(), disabled=True)
        
        # 🟢 الملاحظات في سطر مستقل وبحجم أكبر
        st.text_area("ملاحظات إضافية تفصيلية", placeholder="اكتب تفاصيل طلبك هنا...", height=100)
        
        if req_type in ["تعديل مهنة", "إنهاء خدمة"]:
            st.markdown("<div style='margin-top:10px; color:#5d5fef; font-size:13px;'>📎 يرجى إرفاق المستندات الداعمة</div>", unsafe_allow_html=True)
            st.file_uploader("تحميل المرفقات", type=['pdf', 'png', 'jpg'], key="file_up", label_visibility="collapsed")
        
        st.markdown("<br><b>✍️ التوقيع الرقمي</b>", unsafe_allow_html=True)
        c9, c10 = st.columns([3, 1])
        with c9: st.file_uploader("توقيعك", type=['png', 'jpg'], key="sig_up", label_visibility="collapsed")
        with c10: submit_btn = st.button("إرسال الطلب", use_container_width=True)
        st.markdown('</div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # التحويل التلقائي والنجاح (ثابت في مكانه)
    if submit_btn:
        st.markdown('<div class="step-block"><div class="step-icon">✓</div>', unsafe_allow_html=True)
        with st.container():
            p_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                p_bar.progress(i + 1)
            st.success("🎉 تم إرسال طلبك بنجاح!")
            time.sleep(2)
            st.session_state.page = 'tracking'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحات الأخرى (ثابتة كما هي) ---
elif st.session_state.page == 'tracking':
    st.markdown("<h3 style='text-align:right;'>🔍 سجل الطلبات والمتابعة</h3>", unsafe_allow_html=True)
    st.markdown('<table class="styled-table"><thead><tr><th>رقم الطلب</th><th>النوع</th><th>التاريخ</th><th>الحالة</th></tr></thead><tbody><tr><td>#1028</td><td>تعديل مهنة</td><td>2023-12-20</td><td>قيد الاعتماد</td></tr></tbody></table>', unsafe_allow_html=True)

elif st.session_state.page == 'approvals':
    st.markdown("<h3 style='text-align:right;'>✅ نظام الاعتمادات والموافقات</h3>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="form-body">', unsafe_allow_html=True)
        ac1, ac2, ac3 = st.columns(3)
        with ac1: st.selectbox("إعتماد المدير المباشر", ["قيد الانتظار", "موافق", "مرفوض"])
        with ac2: st.selectbox("إعتماد الموارد البشرية", ["قيد الانتظار", "موافق", "مرفوض"])
        with ac3: st.selectbox("إعتماد المدير العام", ["قيد الانتظار", "موافق", "مرفوض"])
        st.button("تحديث الحالة", use_container_width=True)
        st.markdown('</div></div>', unsafe_allow_html=True)


