import streamlit as st
import pandas as pd
import pickle
import requests
import io

# دالة لتحميل الموديل من جوجل درايف باستخدام الرابط اللي بعتيه
@st.cache_resource
def load_model():
    file_id = '1MQDoy1-5vH4spDp0a10S2sVTUZma2mbT'
    url = f'https://drive.google.com/uc?id={file_id}'
    response = requests.get(url)
    return pickle.load(io.BytesIO(response.content))

st.set_page_config(page_title="منصة أمان", layout="centered")

st.title("🛡️ منصة أمان")
st.subheader("الكشف المبكر عن التنمر الإلكتروني")

try:
    model = load_model()
    st.success("✅ النظام جاهز للتحليل")
    
    user_input = st.text_area("أدخل النص المراد تحليله هنا:")
    
    if st.button("تحليل النص"):
        if user_input:
            # هنا بنفذ التوقع باستخدام الموديل
            prediction = model.predict([user_input])
            result = "نص يحتوي على تنمر" if prediction[0] == 1 else "نص آمن"
            st.warning(f"النتيجة: {result}")
        else:
            st.error("من فضلك أدخل نصاً أولاً")

except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل الموديل: {e}")
