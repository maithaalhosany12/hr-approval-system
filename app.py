import streamlit as st
from datetime import datetime
import time

# 1. إعداد الصفحة (إخفاء القائمة الجانبية وتوسيع العرض)
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="collapsed")

# 2. تنسيق CSS مكثف لتصغير كافة المساحات
st.markdown("""
    <style>
    /* تصغير مساحة الصفحة العامة */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    
    /* تصغير الهيدر الخاص بالشركة */
    .company-header {
        display: flex; align-items: center; justify-content: space-between;
        padding: 8px 20px; background: white; border-radius: 10px; margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-right: 4px solid #5d5fef;
    }

    /* الخط العمودي والدوائر (تصغير الحجم) */
    .step-block { position: relative; padding-right: 45px; margin-bottom: 15px; }
    .step-block::before {
        content: ""; position: absolute; right: 22px; top: 30px; bottom: -25px;
        width: 2px; background-color: #5d5fef; z-index: 1; opacity: 0.2;
    }
    .step-block:last-child::before { display: none; }
    .step-icon {
        position: absolute; right: 5px; top: 0;
        width: 34px; height: 34px; border-radius: 50%;
        background-color: #5d5fef; color: white;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; z-index: 3; font-size: 16px;
    }

    /* تصغير البطاقة وشريط العنوان */
    .content-box { background-color: white; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); overflow: hidden; border: 1px solid #eee; }
    .step-header { background: #5d5fef; color: white; padding: 6px 20px; font-size: 15px; font-weight: bold; }
    .form-body { padding: 12px 20px; }

    /* تصغير الحقول والمسافات بينها */
    .stTextInput>div>div>input, .stSelectbox>div>div>div { min-height: 32px !important; font-size: 14px !important; }
    div[data-testid="stVerticalBlock"] { gap: 0.5rem !important; }
    
    /* زر الإرسال المدمج */
    .stButton>button { height: 2.8em !important; font-size: 14px !important; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'form'

# 5. الهيدر المدمج
st.markdown(f"""
    <div class="company-header">
        <div style="display: flex; align-items: center;">
            <img src="https://cdn-icons-png.flaticon.com/512/281/281764.png" width="30">
            <div style="margin-right: 12px;">
                <span style="font-weight: bold; font-size: 16px;">مؤسسة المسار</span>
                <span style="font-size: 12px; color: #666; margin-right: 10px;">| شؤون الموظفين</span>
            </div>
        </div>
        <div style="font-size: 12px; color: #5d5fef; font-weight: bold;">{datetime.now().strftime('%Y-%m-%d')}</div>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    choice = st.selectbox("", ["تقديم طلب جديد", "متابعة الطلبات"], label_visibility="collapsed")
    if choice == "متابعة الطلبات": st.session_state.page = 'tracking'

# --- صفحة النموذج المدمجة ---
if st.session_state.page == 'form':
    
    # الخطوة 1
    st.markdown('<div class="step-block"><div class="step-icon">1</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">👤 بيانات مقدم الطلب</div><div class="form-body">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4) # توزيع الحقول على 4 أعمدة لتقليل الارتفاع
        job_num = c1.text_input("الرقم الوظيفي")
        name = c2.text_input("الاسم الكامل")
        title = c3.text_input("المسمى")
        dept = c4.text_input("القسم")
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # الخطوة 2
    st.markdown('<div class="step-block"><div class="step-icon">2</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">📝 تفاصيل الطلب والاعتماد</div><div class="form-body">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 2])
        req_type = c1.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
        eff_date = c2.date_input("تاريخ السريان", value=datetime.now(), disabled=True)
        sig_file = c3.file_uploader("ارفق صورة التوقيع", type=['png', 'jpg'], label_visibility="visible")
        
        notes = st.text_input("ملاحظات إضافية (اختياري)") # تحويل text_area إلى text_input لتوفير مساحة
        
        if st.button("إرسال الطلب"):
            if job_num and name and sig_file:
                st.toast("✅ تم الإرسال!", icon="🎉")
                time.sleep(0.5)
                st.session_state.page = 'tracking'
                st.rerun()
            else:
                st.error("⚠️ أكمل البيانات")
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التتبع المدمجة ---
elif st.session_state.page == 'tracking':
    st.markdown("<h5 style='margin-bottom:15px;'>🔍 تتبع الطلب</h5>", unsafe_allow_html=True)
    
    # Timeline مدمج
    st.markdown("""
        <div style="display: flex; justify-content: space-around; background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <div style="text-align: center;"><div style="width:12px; height:12px; background:#5d5fef; border-radius:50%; margin: 0 auto 5px;"></div><div style="font-size:11px;">تقديم</div></div>
            <div style="text-align: center;"><div style="width:12px; height:12px; background:#5d5fef; border-radius:50%; margin: 0 auto 5px;"></div><div style="font-size:11px;">HR</div></div>
            <div style="text-align: center;"><div style="width:12px; height:12px; background:#ddd; border-radius:50%; margin: 0 auto 5px;"></div><div style="font-size:11px;">اعتماد</div></div>
            <div style="text-align: center;"><div style="width:12px; height:12px; background:#ddd; border-radius:50%; margin: 0 auto 5px;"></div><div style="font-size:11px;">اكتمال</div></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("الطلب قيد المراجعة")
    if st.button("عودة"):
        st.session_state.page = 'form'
        st.rerun()
