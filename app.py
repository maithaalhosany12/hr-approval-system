import streamlit as st
from datetime import datetime
import time

# 1. إعداد الصفحة (توسيط المحتوى)
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="collapsed")

# 2. تنسيق CSS: تقصير عرض البطاقات + المحاذاة لليمين + تصغير الحقول
st.markdown("""
    <style>
    /* توجيه الصفحة بالكامل من اليمين لليسار */
    .main { background-color: #f4f7f9; direction: rtl; }
    div[data-testid="stVerticalBlock"] { direction: rtl; }
    
    /* تقصير عرض الحاوية الرئيسية لتكون في المنتصف وملمومة */
    .block-container { max-width: 900px !important; padding-top: 2rem; }

    /* تقليص ارتفاع الحقول */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        min-height: 32px !important; height: 32px !important;
        padding: 0px 10px !important; font-size: 14px !important;
        text-align: right;
    }

    /* هيدر الشركة */
    .company-header {
        display: flex; align-items: center; justify-content: space-between;
        padding: 10px 20px; background: white; border-radius: 12px; margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-right: 6px solid #5d5fef;
        direction: rtl;
    }

    /* السلم الجانبي على جهة اليمين */
    .step-block { position: relative; padding-right: 55px; margin-bottom: 20px; text-align: right; }
    .step-block::before {
        content: ""; position: absolute; right: 24px; top: 40px; bottom: -35px;
        width: 2px; background-color: #5d5fef; z-index: 1; opacity: 0.2;
    }
    .step-block:last-child::before { display: none; }

    .step-icon {
        position: absolute; right: 5px; top: 0;
        width: 38px; height: 38px; border-radius: 50%;
        background-color: #5d5fef; color: white;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; z-index: 3; font-size: 18px;
    }

    /* بطاقة المحتوى (مقصرة العرض) */
    .content-box { 
        background-color: white; border-radius: 12px; 
        box-shadow: 0 6px 15px rgba(0,0,0,0.04); overflow: hidden; 
        border: 1px solid #eef0f2; text-align: right;
    }
    .step-header { 
        background: linear-gradient(90deg, #7a7cfc, #5d5fef); 
        color: white; padding: 8px 20px; font-size: 15px; font-weight: bold;
        text-align: right;
    }
    .form-body { padding: 15px 20px; }

    /* مراجعة النصوص لتكون لليمين */
    label { text-align: right !important; width: 100%; display: block !important; }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'form'

# 5. الهيدر (يمين)
st.markdown(f"""
    <div class="company-header">
        <div style="display: flex; align-items: center;">
            <div style="background:#5d5fef; padding:5px; border-radius:8px; margin-left:12px;">
                <img src="https://cdn-icons-png.flaticon.com/512/281/281764.png" width="25" style="filter: brightness(0) invert(1);">
            </div>
            <div>
                <div style="font-weight: bold; font-size: 16px;">مؤسسة المسار المتكامل</div>
                <div style="font-size: 11px; color: #666;">قسم الموارد البشرية</div>
            </div>
        </div>
        <div style="font-size: 12px; color: #5d5fef; font-weight: bold;">{datetime.now().strftime('%Y-%m-%d')}</div>
    </div>
    """, unsafe_allow_html=True)

# القائمة الجانبية
with st.sidebar:
    choice = st.selectbox("", ["تقديم طلب جديد", "متابعة الطلبات"], label_visibility="collapsed")
    if choice == "متابعة الطلبات": st.session_state.page = 'tracking'

# --- صفحة النموذج (محاذاة يمين + عرض مقلص) ---
if st.session_state.page == 'form':
    
    # الخطوة 1
    st.markdown('<div class="step-block"><div class="step-icon">1</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">👤 بيانات مقدم الطلب</div><div class="form-body">', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        job_num = c1.text_input("الرقم الوظيفي")
        full_name = c2.text_input("الاسم الكامل")
        
        c3, c4 = st.columns(2)
        job_title = c3.text_input("المسمى الوظيفي")
        unit = c4.text_input("الوحدة / القسم")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # الخطوة 2
    st.markdown('<div class="step-block"><div class="step-icon">2</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box"><div class="step-header">📝 تفاصيل موضوع الطلب والاعتماد</div><div class="form-body">', unsafe_allow_html=True)
        
        c5, c6 = st.columns(2)
        req_type = c5.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
        eff_date = c6.date_input("تاريخ السريان (تلقائي)", value=datetime.now(), disabled=True)
        
        st.markdown("<div style='text-align:right; font-size:14px; font-weight:bold; margin-top:10px;'>✍️ صورة التوقيع الرقمي</div>", unsafe_allow_html=True)
        sig_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        
        notes = st.text_input("ملاحظات إضافية")
        
        st.markdown("<br>", unsafe_allow_html=True)
        # زر الإرسال جهة اليمين
        c_btn, _ = st.columns([1, 3])
        if c_btn.button("إرسال الطلب الآن"):
            if job_num and full_name and sig_file:
                st.toast("✅ تم إرسال طلبك بنجاح!", icon="🎉")
                time.sleep(1)
                st.session_state.page = 'tracking'
                st.rerun()
            else:
                st.error("⚠️ يرجى تعبئة البيانات المطلوبة")
                
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التتبع ---
elif st.session_state.page == 'tracking':
    st.markdown("<h5 style='text-align:right;'>🔍 تتبع حالة الطلب</h5>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="display: flex; justify-content: space-around; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); direction: rtl;">
            <div style="text-align: center;"><div style="width:20px; height:20px; background:#5d5fef; border-radius:50%; margin: 0 auto 8px;"></div><div style="font-size:12px; font-weight:bold;">تقديم</div></div>
            <div style="text-align: center;"><div style="width:20px; height:20px; background:#5d5fef; border-radius:50%; margin: 0 auto 8px;"></div><div style="font-size:12px; font-weight:bold;">مراجعة</div></div>
            <div style="text-align: center;"><div style="width:20px; height:20px; background:#ddd; border-radius:50%; margin: 0 auto 8px;"></div><div style="font-size:12px; font-weight:bold;">اعتماد</div></div>
            <div style="text-align: center;"><div style="width:20px; height:20px; background:#ddd; border-radius:50%; margin: 0 auto 8px;"></div><div style="font-size:12px; font-weight:bold;">اكتمال</div></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("طلبك حالياً قيد التدقيق.")
    if st.button("العودة"):
        st.session_state.page = 'form'
        st.rerun()
