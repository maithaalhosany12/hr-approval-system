import streamlit as st
from fpdf import FPDF
import arabic_reshaper
from bidi.algorithm import get_display
import io

# --- 1. إعدادات الصفحة والتصميم ---
st.set_page_config(page_title="نظام إدارة الطلبات الرسمي", layout="centered")

# تعريف المتغيرات في session_state إذا لم تكن موجودة
if 'page' not in st.session_state:
    st.session_state.page = 'request'
if 'stage' not in st.session_state:
    st.session_state.stage = 2  # تبدأ من 2 تعني (بانتظار المعتمد الأول)
if 'order_id' not in st.session_state:
    st.session_state.order_id = "REQ-88204"

# --- 2. دالة معالجة النصوص العربية للـ PDF ---
def format_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

# --- 3. دالة إنشاء ملف PDF الرسمي ---
def generate_official_pdf():
    pdf = FPDF()
    pdf.add_page()
    # إضافة شعار تخيلي (يمكنك استبدال 'logo.png' بملفك)
    # pdf.image("logo.png", x=10, y=8, w=30) 
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Official Request Summary", 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Order Reference: {st.session_state.order_id}", 0, 1, 'L')
    pdf.cell(0, 10, f"Status: Under Review - Stage {st.session_state.stage}", 0, 1, 'L')
    pdf.ln(10)
    
    # قسم التواقيع
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(60, 10, "Employee", 1, 0, 'C')
    pdf.cell(60, 10, "Manager Approval", 1, 0, 'C')
    pdf.cell(60, 10, "HR Director", 1, 1, 'C')
    pdf.cell(60, 20, "", 1, 0)
    pdf.cell(60, 20, "", 1, 0)
    pdf.cell(60, 20, "", 1, 1)
    
    return pdf.output()

# --- 4. واجهة المستخدم ---

# القائمة العلوية للتنقل
col1, col2 = st.columns(2)
with col1:
    if st.button("📝 تقديم طلب جديد", use_container_width=True):
        st.session_state.page = 'request'
with col2:
    if st.button("🔍 تتبع حالة الطلب", use_container_width=True):
        st.session_state.page = 'tracking'

st.divider()

# --- صفحة تقديم الطلب ---
if st.session_state.page == 'request':
    st.header("إرسال طلب جديد")
    with st.form("request_form"):
        name = st.text_input("اسم الموظف")
        req_type = st.selectbox("نوع الطلب", ["إجازة", "نقل داخلي", "عهدة"])
        reason = st.text_area("السبب")
        submitted = st.form_submit_button("إرسال الطلب")
        if submitted:
            st.success(f"تم إرسال الطلب بنجاح! رقم المرجع: {st.session_state.order_id}")
            st.session_state.stage = 2 # ينتقل للمرحلة الثانية تلقائياً

# --- صفحة تتبع الطلبات (المطلوبة) ---
elif st.session_state.page == 'tracking':
    st.markdown("### 🚦 مسار الاعتمادات الإدارية")
    
    # تصميم الـ Timeline باستخدام HTML و CSS
    st.markdown("""
        <style>
        .timeline { border-right: 3px solid #ddd; padding-right: 30px; margin-right: 20px; position: relative; }
        .step-container { position: relative; margin-bottom: 45px; }
        .step-circle { 
            position: absolute; right: -42px; top: 0; width: 22px; height: 22px; 
            border-radius: 50%; background: #fff; border: 3px solid #ddd; z-index: 10;
        }
        .step-completed { background: #28a745; border-color: #28a745; color: white; text-align: center; font-size: 14px; line-height: 18px; }
        .step-active { background: #007bff; border-color: #007bff; box-shadow: 0 0 10px rgba(0,123,255,0.5); }
        .step-content { direction: rtl; text-align: right; }
        .step-title { font-weight: bold; font-size: 1.1em; color: #333; }
        .step-desc { font-size: 0.9em; color: #666; }
        .waiting-label { color: #d63031; font-weight: bold; font-size: 0.8em; }
        </style>
    """, unsafe_allow_html=True)

    # بناء مراحل التتبع
    stages_info = [
        {"title": "تقديم الطلب", "desc": "تم استلام الطلب في النظام", "target": 1},
        {"title": "المعتمد الأول (المدير المباشر)", "desc": "قيد المراجعة الفنية", "target": 2},
        {"title": "المعتمد الثاني (مدير القسم)", "desc": "التدقيق الإداري", "target": 3},
        {"title": "مدير الموارد البشرية", "desc": "الاعتماد النهائي وإغلاق الطلب", "target": 4},
    ]

    st.markdown('<div class="timeline">', unsafe_allow_html=True)
    
    for s in stages_info:
        status_class = ""
        icon = ""
        waiting_text = ""
        
        if st.session_state.stage > s['target']:
            status_class = "step-completed"
            icon = "✓"
        elif st.session_state.stage == s['target']:
            status_class = "step-active"
            waiting_text = f" <span class='waiting-label'>(بانتظار {s['title']})</span>"
        
        st.markdown(f"""
            <div class="step-container">
                <div class="step-circle {status_class}">{icon}</div>
                <div class="step-content">
                    <div class="step-title">{s['title']} {waiting_text}</div>
                    <div class="step-desc">{s['desc']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # زر التحويل لـ PDF
    st.divider()
    pdf_data = generate_official_pdf()
    st.download_button(
        label="🖨️ طباعة الطلب (PDF رسمي)",
        data=pdf_data,
        file_name=f"Order_{st.session_state.order_id}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    # تحكم وهمي للمحاكاة (لتجربة تغيير المراحل)
    with st.expander("🛠️ لوحة تحكم المحاكاة (للمطور فقط)"):
        new_stage = st.slider("تغيير مرحلة الطلب يدوياً", 1, 4, st.session_state.stage)
        if st.button("تحديث الحالة"):
            st.session_state.stage = new_stage
            st.rerun()
