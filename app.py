import streamlit as st
from datetime import datetime
import time
import random

# 1. إعداد الصفحة والتنسيق (ثابت تماماً كما تحبين)
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
        box-shadow: 0 4px 10px rgba(93,95,239,0.3);
    }

    .content-box { background-color: white; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.04); overflow: hidden; border: 1px solid #eef0f2; }
    .step-header { background: linear-gradient(90deg, #5d5fef, #7a7cfc); color: white; padding: 12px 25px; font-size: 15px; font-weight: bold; }
    .form-body { padding: 20px 25px; }

    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input { min-height: 32px !important; height: 32px !important; text-align: right !important; border-radius: 8px !important; }
    .stTextArea>div>div>textarea { border-radius: 8px !important; text-align: right !important; font-size: 14px !important; }
    label { font-size: 12px !important; font-weight: bold !important; color: #475569 !important;}
    
    .attachment-box { background-color: #fff9e6; border: 1px dashed #ffd43b; padding: 10px; border-radius: 8px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'form'
if 'stage' not in st.session_state: st.session_state.stage = 1
if 'order_id' not in st.session_state: st.session_state.order_id = f"REQ-{random.randint(1000, 9999)}"

# الهيدر
st.markdown('<div class="company-header"><div class="header-logo"><img src="https://cdn-icons-png.flaticon.com/512/281/281764.png"></div><div class="header-text"><h1>مؤسسة المسار المتكامل</h1><p>قسم الموارد البشرية - نموذج الطلبات الإلكتروني</p></div></div>', unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    st.title("⚙️ الإجراءات")
    choice = st.selectbox("انتقل إلى:", ["تقديم طلب جديد", "متابعة الطلبات", "الاعتمادات"], index=0 if st.session_state.page == 'form' else 1 if st.session_state.page == 'tracking' else 2)
    st.session_state.page = 'form' if choice == "تقديم طلب جديد" else 'tracking' if choice == "متابعة الطلبات" else 'approvals'

# --- 1. صفحة النموذج (مع ميزة المرفق الشرطي) ---
if st.session_state.page == 'form':
    # الخطوة 1: البيانات الشخصية
    st.markdown('<div class="step-block"><div class="step-icon">1</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">👤 الخطوة الأولى: بيانات مقدم الطلب</div><div class="form-body">', unsafe_allow_html=True)
        r1, _ = st.columns([1, 4])
        with r1: st.text_input("رقم الطلب", value=st.session_state.order_id, disabled=True)
        
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1: st.text_input("الرقم الوظيفي")
        with c2: st.text_input("الاسم الكامل")
        with c3: st.text_input("المسمى")
        with c4: st.text_input("القسم")
        with c5: st.date_input("تاريخ التعيين")
        st.markdown('</div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # الخطوة 2: تفاصيل الطلب والمرفقات
    st.markdown('<div class="step-block"><div class="step-icon">2</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">📝 الخطوة الثانية: تفاصيل الطلب</div><div class="form-body">', unsafe_allow_html=True)
        c6, c7 = st.columns([1, 1])
        with c6: 
            req_type = st.selectbox("نوع الطلب", ["نقل داخلي", "تعديل مهنة", "إنهاء خدمة"])
        with c7: 
            st.date_input("تاريخ السريان", value=datetime.now(), disabled=True)
        
        # منطق المرفق: يظهر فقط في حال تعديل مهنة أو إنهاء خدمة
        if req_type in ["تعديل مهنة", "إنهاء خدمة"]:
            st.markdown('<div class="attachment-box">⚠️ <b>مرفق مطلوب:</b> يرجى إرفاق المستندات الداعمة لطلب ({}).</div>'.format(req_type), unsafe_allow_html=True)
            st.file_uploader("تحميل المرفق الرسمي (PDF/JPG)", type=['pdf', 'png', 'jpg'], key="req_attachment")
        
        st.text_area("ملاحظات إضافية تفصيلية", height=100)
        
        st.markdown("<br><b>✍️ التوقيع الرقمي</b>", unsafe_allow_html=True)
        c9, c10 = st.columns([3, 1])
        with c9: st.file_uploader("توقيعك الشخصي", type=['png', 'jpg'], key="sig_up", label_visibility="collapsed")
        with c10: submit_btn = st.button("إرسال الطلب", use_container_width=True)
        st.markdown('</div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if submit_btn:
        st.success(f"🎉 تم إرسال طلبك رقم ({st.session_state.order_id}) بنجاح!")
        time.sleep(2)
        st.session_state.page = 'tracking'
        st.rerun()

# --- باقي الصفحات (المتابعة والاعتمادات) تبقى كما هي في الكود السابق ---
elif st.session_state.page == 'tracking':
    st.markdown("### 🔍 سجل المتابعة")
    # ... كود الجدول السابق ...

elif st.session_state.page == 'approvals':
    st.markdown("### ✅ نظام الاعتمادات")
    # ... كود الاعتمادات السابق ...
