import streamlit as st
from datetime import datetime
import time

# 1. إعداد الصفحة (عرض واسع واتجاه يمين)
st.set_page_config(page_title="نظام شؤون الموظفين", layout="wide", initial_sidebar_state="collapsed")

# 2. تنسيق CSS ثابت (لا يتغير فيه الاتجاه)
st.markdown("""
    <style>
    /* فرض اتجاه اليمين على كل شيء */
    .main { direction: rtl !important; text-align: right !important; background-color: #f8fafc; }
    div[data-testid="stVerticalBlock"] { direction: rtl !important; }
    
    /* تقليص عرض المحتوى ليكون ملموماً ومرتباً في المنتصف */
    .block-container { max-width: 850px !important; padding-top: 2rem; }

    /* الهيدر: الشعار والنص في المنتصف */
    .header-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        background: white; padding: 20px; border-radius: 15px; margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); text-align: center;
    }
    .header-container img { width: 50px; margin-bottom: 10px; }
    .header-container h1 { margin: 0; font-size: 20px; color: #1e293b; }
    .header-container p { margin: 0; font-size: 13px; color: #5d5fef; font-weight: bold; }

    /* بطاقة الخطوات (النمط القديم الفخم) */
    .step-card {
        background: white; border-radius: 12px; overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;
        margin-bottom: 25px; direction: rtl;
    }

    /* شريط العنوان مع الرقم على اليسار */
    .step-bar {
        background: linear-gradient(90deg, #5d5fef, #7a7cfc);
        color: white; padding: 10px 20px; display: flex;
        justify-content: space-between; align-items: center;
    }
    .step-num {
        width: 28px; height: 28px; background: rgba(255,255,255,0.2);
        border: 1px solid white; border-radius: 50%;
        display: flex; align-items: center; justify-content: center; font-size: 14px;
    }

    /* تقصير عرض مربعات التعبئة وتنسيقها */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        min-height: 35px !important; height: 35px !important;
        text-align: right !important; direction: rtl !important;
        font-size: 14px !important; border-radius: 8px !important;
    }

    /* محاذاة العناوين (Labels) لليمين */
    label { text-align: right !important; width: 100%; display: block !important; font-weight: 600 !important; color: #475569 !important; }
    
    .body-padding { padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

# إدارة الصفحات
if 'page' not in st.session_state:
    st.session_state.page = 'form'

# 3. الهيدر (الشعار في الوسط والكتابة تحته)
st.markdown("""
    <div class="header-container">
        <img src="https://cdn-icons-png.flaticon.com/512/281/281764.png">
        <h1>مؤسسة المسار المتكامل</h1>
        <p>قسم شؤون الموظفين - نموذج الطلبات الإلكتروني</p>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    choice = st.selectbox("", ["تقديم طلب جديد", "متابعة الطلبات"], label_visibility="collapsed")
    if choice == "متابعة الطلبات": st.session_state.page = 'tracking'

# --- الصفحة الأولى: النموذج ---
if st.session_state.page == 'form':
    
    # الخطوة 1
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-bar"><span>👤 الخطوة الأولى: بيانات مقدم الطلب</span><div class="step-num">1</div></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="body-padding">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: job_num = st.text_input("الرقم الوظيفي")
        with c2: name = st.text_input("الاسم الكامل")
        
        c3, c4 = st.columns(2)
        with c3: title = st.text_input("المسمى الوظيفي")
        with c4: dept = st.text_input("الوحدة / القسم")
        st.markdown('</div></div></div>', unsafe_allow_html=True)

    # الخطوة 2
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-bar"><span>📝 الخطوة الثانية: تفاصيل الطلب والاعتماد</span><div class="step-num">2</div></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="body-padding">', unsafe_allow_html=True)
        c5, c6 = st.columns(2)
        with c5: req_type = st.selectbox("نوع الطلب", ["نقل", "تغيير مهنة", "إنهاء خدمة"])
        with c6: eff_date = st.date_input("تاريخ السريان (تلقائي)", value=datetime.now(), disabled=True)
        
        st.markdown("<p style='margin-bottom:5px; font-weight:bold; font-size:14px;'>✍️ ارفع صورة التوقيع الرقمي</p>", unsafe_allow_html=True)
        sig_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        
        notes = st.text_input("ملاحظات إضافية (اختياري)")
        
        st.markdown("<br>", unsafe_allow_html=True)
        # زر الإرسال مقلص العرض
        btn_col, _ = st.columns([1, 3])
        if btn_col.button("إرسال الطلب الآن"):
            if job_num and name and sig_file:
                st.toast("✅ تم إرسال طلبك بنجاح!", icon="🎉")
                time.sleep(1)
                st.session_state.page = 'tracking'
                st.rerun()
            else:
                st.error("⚠️ يرجى إكمال البيانات ورفع صورة التوقيع")
        st.markdown('</div></div></div>', unsafe_allow_html=True)

# --- الصفحة الثانية: التتبع ---
elif st.session_state.page == 'tracking':
    st.markdown("<h4 style='text-align:right;'>🔍 حالة الطلبات المقدمة</h4>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="display: flex; justify-content: space-around; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); direction: rtl; margin-top: 20px;">
            <div style="text-align: center;"><div style="width:25px; height:25px; background:#5d5fef; border-radius:50%; margin: 0 auto 10px; box-shadow: 0 0 10px #5d5fef;"></div><div style="font-size:13px; font-weight:bold;">تم التقديم</div></div>
            <div style="text-align: center;"><div style="width:25px; height:25px; background:#5d5fef; border-radius:50%; margin: 0 auto 10px; box-shadow: 0 0 10px #5d5fef;"></div><div style="font-size:13px; font-weight:bold;">مراجعة HR</div></div>
            <div style="text-align: center;"><div style="width:25px; height:25px; background:#ddd; border-radius:50%; margin: 0 auto 10px;"></div><div style="font-size:13px; font-weight:bold;">الاعتماد</div></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("الطلب قيد المراجعة الفنية حالياً.")
    if st.button("العودة للرئيسية"):
        st.session_state.page = 'form'
        st.rerun()
