import streamlit as st
import pandas as pd
import pickle
import gdown
import os

# دالة تحميل الموديل الجديد من الدرايف
@st.cache_resource
def load_model():
    file_id = '1jLjUy1EEdrpmVcF5g564vTojYaVVGZZR'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'baseera_model.pkl'
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    with open(output, 'rb') as f:
        return pickle.load(f)

# إعدادات الواجهة باسم "بصيرة"
st.set_page_config(page_title="منصة بصيرة", layout="wide")

# تنسيق العنوان
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🛡️ منصة بَصيرة</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>التحليل الذكي لبيانات التنمر المدرسي</h3>", unsafe_allow_html=True)
st.write("---")

try:
    model = load_model()
    
    st.info("الرجاء اختيار البيانات التالية لتحليل حالة الطالب:")

    # تقسيم الخانات لصفوف وأعمدة عشان شكل الموقع يبقى منظم
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
    if st.button("بدء تحليل البيانات"):
        # تحويل الاختيارات النصية لأرقام للموديل (Mapping)
        mapping = {"نعم": 1, "لا": 0, "ذكر": 1, "أنثى": 0}
        
        # ترتيب المدخلات الـ 13 بالضبط زي ما الموديل اتدرب في الكولاب
        inputs = [
            mapping[outside], 
            mapping[cyber], 
            age, 
            mapping[sex],
            mapping[attacked], 
            mapping[lonely], 
            friends,
            mapping[miss], 
            mapping[kind], 
            mapping[parents],
            1 if underweight else 0, 
            1 if overweight else 0, 
            1 if obese else 0
        ]
        
        prediction = model.predict([inputs])
        
        st.markdown("### النتيجة النهائية:")
        if prediction[0] == 1:
            st.error("⚠️ مؤشر مرتفع: توجد احتمالية لتعرض الطالب للتنمر. يوصى بالمتابعة التربوية.")
        else:
            st.success("✅ مؤشر آمن: لا توجد مؤشرات قوية على تعرض الطالب للتنمر حالياً.")

except Exception as e:
    st.error("نعتذر، هناك مشكلة في تحميل الموديل. تأكدي أن الملف متاح للجميع على الدرايف.")
