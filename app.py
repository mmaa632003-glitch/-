import streamlit as st
import pandas as pd
import pickle
import gdown
import os

# --- 1. إعدادات الواجهة والألوان (CSS) ---
def local_css():
    st.markdown(
        """
        <style>
        /* الخلفية العامة */
        .stApp {
            background-color: #F8FAFC;
        }
        /* تنسيق العناوين */
        h1 {
            color: #1E3A8A !important;
            font-family: 'Cairo', sans-serif;
            text-align: center;
        }
        h2 {
            color: #1E3A8A !important;
            text-align: center;
        }
        /* تنسيق الأزرار */
        .stButton>button {
            background-color: #1E3A8A;
            color: white;
            border-radius: 12px;
            width: 100%;
            height: 50px;
            font-size: 18px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #2563EB;
            color: white;
        }
        /* صندوق النتائج */
        .result-box {
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

local_css()

# --- 2. دالة تحميل الموديل والمنشورات التوعوية ---
@st.cache_resource
def load_model():
    # الـ ID بتاع الموديل اللي رفعناه قبل كدة
    file_id = '1jLjUy1EEdrpmVcF5g564vTojYaVVGZZR'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'baseera_model.pkl'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    with open(output, 'rb') as f:
        return pickle.load(f)

# --- 3. واجهة البرنامج الرئيسية ---
st.markdown("<h1>🛡️ منصة بَصيرة الذكية</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B;'>مشروع التخرج: الكشف عن التنمر المدرسي باستخدام تعلم الآلة</p>", unsafe_allow_html=True)
st.write("---")

try:
    model = load_model()
    
    # قسم إدخال البيانات
    st.subheader("📋 نموذج تحليل حالة الطالب")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("عمر الطالب", 10, 25, 15)
        sex = st.selectbox("الجنس", ["أنثى", "ذكر"])
        cyber = st.selectbox("هل تعرض الطالب لتنمر إلكتروني سابقاً؟", ["لا", "نعم"])
        lonely = st.selectbox("هل يشعر الطالب بالوحدة معظم الوقت؟", ["لا", "نعم"])
        attacked = st.selectbox("هل تعرض الطالب لهجوم جسدي؟", ["لا", "نعم"])
        outside = st.selectbox("هل حدث تنمر خارج أسوار المدرسة؟", ["لا", "نعم"])

    with col2:
        friends = st.number_input("عدد الأصدقاء المقربين", 0, 10, 3)
        parents = st.selectbox("هل الأهل يتفهمون مشاكل الطالب؟", ["نعم", "لا"])
        kind = st.selectbox("هل الزملاء في المدرسة متعاونون؟", ["نعم", "لا"])
        miss = st.selectbox("هل تغيب الطالب عن المدرسة بدون إذن؟", ["لا", "نعم"])
        underweight = st.checkbox("هل يعاني الطالب من نقص وزن؟")
        overweight = st.checkbox("هل يعاني الطالب من وزن زائد؟")
        obese = st.checkbox("هل يعاني الطالب من سمنة مفرطة؟")

    st.write("---")
    
    if st.button("إجراء التحليل الإحصائي الآن"):
        # تحويل النصوص لأرقام للموديل
        mapping = {"نعم": 1, "لا": 0, "ذكر": 1, "أنثى": 0}
        
        inputs = [
            mapping[outside], mapping[cyber], age, mapping[sex],
            mapping[attacked], mapping[lonely], friends,
            mapping[miss], mapping[kind], mapping[parents],
            1 if underweight else 0, 1 if overweight else 0, 1 if obese else 0
        ]
        
        prediction = model.predict([inputs])
        
        st.markdown("### 📊 نتيجة التحليل:")
        if prediction[0] == 1:
            st.error("⚠️ مؤشر مرتفع: هناك احتمالية لتعرض الطالب للتنمر. يوصى بالتدخل التربوي.")
        else:
            st.success("✅ مؤشر آمن: لا توجد مؤشرات قلق واضحة بشأن تعرض الطالب للتنمر حالياً.")

except Exception as e:
    st.error(f"عذراً، حدث خطأ فني: {e}")

# --- 4. معرض بصيرة التوعوي (الصور الـ 6) ---
st.write("---")
st.markdown("<h2>💡 معرض بَصيرة التوعوي</h2>", unsafe_allow_html=True)

# قائمة الـ IDs اللي بعتيها للصور
image_ids = [
    "1M9iTdFQgKKzd4Jp1y9j3HE5NK0sWSv_v",
    "1GHTzjnMo_9hb4Jrr5rxyqOtyuxOsq3mO",
    "1bveQNCSBV399mIZHZHcD8XcDzRqk8MdD",
    "194UUr6XatRELceStckSXM8S1B7Spe9ZD",
    "1ic226ifc_9y93VXUSueVPdG6EK8NSAqK",
    "1H4_gNm_SYW_-Q04p2n3ap0Ac_Kr-mNE_"
]

# عرض الصور في صفوف (3 صور في كل صف)
cols = st.columns(3)
for i, img_id in enumerate(image_ids):
    with cols[i % 3]:
        img_url = f'https://drive.google.com/uc?id={img_id}'
        st.image(img_url, use_container_width=True)

st.markdown("<p style='text-align: center; color: #94A3B8; margin-top: 50px;'>تم التطوير بواسطة: ميوي | مشروع التخرج 2026</p>", unsafe_allow_html=True)
