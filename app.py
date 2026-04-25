import streamlit as st
import pandas as pd
import pickle
import requests
import io

# دالة التحميل النهائية والأكثر أماناً
@st.cache_resource
def load_model():
    # الرابط المباشر النهائي
    file_id = '1MQDoy1-5vH4spDp0a10S2sVTUZma2mbT'
    direct_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    
    try:
        # بنحاول نحمل الملف
        session = requests.Session()
        response = session.get(direct_url, stream=True)
        
        # لو جوجل طلع رسالة تحذير من الفيروسات (بتحصل للملفات الكبيرة)
        token = None
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                token = value
                break
        
        if token:
            final_url = direct_url + f'&confirm={token}'
            response = session.get(final_url, stream=True)
            
        if response.status_code == 200:
            return pickle.load(io.BytesIO(response.content))
        else:
            st.error("جوجل درايف رفض الطلب. تأكد من أن الملف 'عام' Anyone with the link")
            return None
            
    except Exception as e:
        st.error(f"خطأ تقني: {e}")
        return None

st.set_page_config(page_title="منصة أمان", layout="centered")

st.title("🛡️ منصة أمان")
st.subheader("الكشف المبكر عن التنمر الإلكتروني")

model = load_model()

if model:
    st.success("✅ النظام جاهز للتحليل")
    user_input = st.text_area("أدخل النص المراد تحليله هنا:")
    
    if st.button("تحليل النص"):
        if user_input:
            prediction = model.predict([user_input])
            result = "⚠️ نص يحتوي على تنمر" if prediction[0] == 1 else "✅ نص آمن"
            st.write(f"### {result}")
        else:
            st.error("من فضلك أدخل نصاً")
