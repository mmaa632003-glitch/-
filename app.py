import streamlit as st
import pandas as pd
import pickle
import gdown
import os
import requests
from PIL import Image
from io import BytesIO

# --- 1. إعدادات الواجهة والـ CSS ---
def local_css():
    bg_img_id = '1wnNEEi1zq_TvCAvExB3_BmsCZabfoq6e'
    bg_img_url = f'https://drive.google.com/uc?id={bg_img_id}'
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)), 
                        url("{bg_img_url}");
            background-size: cover;
            background-attachment: fixed;
        }}
        h1 {{ color: #1E40AF !important; text-align: center; font-family: 'Cairo', sans-serif; margin-bottom: 5px; }}
        .description {{ color: #1E3A8A; text-align: center; font-size: 1.2rem; font-weight: bold; margin-bottom: 30px; }}
        .stButton>button {{
            background: linear-gradient(90deg, #1E40AF 0%, #3B82F6 100%);
            color: white; border-radius: 20px; font-weight: bold; width: 100%; height: 60px; font-size: 20px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

local_css()

# --- 2. تحميل الموديل ---
@st.cache_resource
def load_model():
    file_id = '1jLjUy1EEdrpmVcF5g564vTojYaVVGZZR'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'baseera_model.pkl'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    with open(output, 'rb') as f:
        return pickle.load(f)

# --- 3. التحكم في التنقل (Navigation) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def change_page(page_name):
    st.session_state.page = page_name

# العناوين والوصف (ثابتة في كل الصفحات)
st.markdown("<h1>🛡️ مَنصة بَصيرة الذكية</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>لتحليل بيانات التنمر المدرسي ودعم الوعي الرقمي</p>", unsafe_allow_html=True)

# --- الشاشة الرئيسية ---
if st.session_state.page == 'home':
    st.write("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 بدء تحليل بيانات الحالة"):
            change_page('analysis')
            
    with col2:
        if st.button("💡 ركن الوعي والإرشاد"):
            change_page('awareness')

# --- صفحة التحليل ---
elif st.session_state.page == 'analysis':
    if st.button("⬅️ العودة للرئيسية"):
        change_page('home')
        
    st.markdown("<h2 style='text-align: center;'>📋 نموذج تحليل الحالة</h2>", unsafe_allow_html=True)
    try:
        model = load_model()
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("عمر الطالب", 10, 25, 15)
            sex = st.selectbox("الجنس", ["أنثى", "ذكر"])
            cyber = st.selectbox("تعرض لتنمر إلكتروني؟", ["لا", "نعم"])
            lonely = st.selectbox("يشعر بالوحدة؟", ["لا", "نعم"])
            attacked = st.selectbox("تعرض لهجوم جسدي؟", ["لا", "نعم"])
            outside = st.selectbox("تنمر خارج المدرسة؟", ["لا", "نعم"])
        with col2:
            friends = st.number_input("عدد الأصدقاء", 0, 10, 3)
            parents = st.selectbox("الأهل يتفهمون المشاكل؟", ["نعم", "لا"])
            kind = st.selectbox("الزملاء متعاونون؟", ["نعم", "لا"])
            miss = st.selectbox("غياب بدون إذن؟", ["لا", "نعم"])
            underweight = st.checkbox("نقص وزن")
            overweight = st.checkbox("وزن زائد")
            obese = st.checkbox("سمنة مفرطة")

        if st.button("🚀 إجراء التحليل الآن"):
            mapping = {"نعم": 1, "لا": 0, "ذكر": 1, "أنثى": 0}
            inputs = [mapping[outside], mapping[cyber], age, mapping[sex], mapping[attacked], mapping[lonely], friends, mapping[miss], mapping[kind], mapping[parents], 1 if underweight else 0, 1 if overweight else 0, 1 if obese else 0]
            prediction = model.predict([inputs])
            if prediction[0] == 1: st.error("⚠️ مؤشر مرتفع لوجود تنمر.")
            else: st.success("✅ حالة آمنة ومستقرة.")
    except Exception as e:
        st.error(f"خطأ: {e}")

# --- صفحة الوعي والإرشاد ---
elif st.session_state.page == 'awareness':
    if st.button("⬅️ العودة للرئيسية"):
        change_page('home')
        
    st.markdown("<h2 style='text-align: center;'>💡 ركن الوعي والإرشاد</h2>", unsafe_allow_html=True)
    image_ids = ["1M9iTdFQgKKzd4Jp1y9j3HE5NK0sWSv_v", "1GHTzjnMo_9hb4Jrr5rxyqOtyuxOsq3mO", "1bveQNCSBV399mIZHZHcD8XcDzRqk8MdD", "194UUr6XatRELceStckSXM8S1B7Spe9ZD", "1ic226ifc_9y93VXUSueVPdG6EK8NSAqK", "1H4_gNm_SYW_-Q04p2n3ap0Ac_Kr-mNE_"]
    
    cols = st.columns(3)
    for i, img_id in enumerate(image_ids):
        with cols[i % 3]:
            try:
                response = requests.get(f'https://drive.google.com/uc?id={img_id}')
                st.image(Image.open(BytesIO(response.content)), use_container_width=True)
            except: st.info(f"إرشاد {i+1}")

st.markdown("<br><p style='text-align: center; color: #1E40AF; font-weight: bold;'>صُنع بواسطة ميوي | مشروع التخرج 2026</p>", unsafe_allow_html=True)
