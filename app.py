import streamlit as st
import time
import requests

# --- 100% मोबाइल-फ्रेंडली ऑटो-फिट स्क्रीन सेटिंग्स ---
st.set_page_config(
    page_title="LEXA", 
    page_icon="⚖️", 
    layout="wide"
)

# --- 200MB हटाने और रिस्पॉन्सिव थीम की कड़क CSS ---
st.markdown("""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Dancing+Script:wght=700&display=swap" rel="stylesheet">
    <style>
        /* 200MB वाले टेक्स्ट को जड़ से छिपाना */
        .stFileUploader small { display: none !important; }
        div[data-testid="stFileUploaderFileData"] small { display: none !important; }
        
        /* मोबाइल और डेस्कटॉप ऑटो-फिट कंटेनर */
        .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; padding-left: 1rem; padding-right: 1rem; max-width: 100%; }
        
        /* डार्क प्रीमियम लीगल थीम */
        html, body, [data-testid="stAppViewContainer"] { background-color: #0f172a; color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

# सेशन स्टेट का रख-रखाव
if 'terms_accepted' not in st.session_state:
    st.session_state.terms_accepted = False
if 'timer_complete' not in st.session_state:
    st.session_state.timer_complete = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Petitioner File"
if 'manual_lawyer_logged' not in st.session_state:
    st.session_state.manual_lawyer_logged = False
if 'gemini_key' not in st.session_state:
    st.session_state.gemini_key = ""

# लाइव जेमिनी एआई इंजन फंक्शन
def call_gemini_ai(user_key, prompt_text):
    try:
        api_url = f"https://googleapis.com{user_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['candidates']['content']['parts']['text']
        else:
            return "⚠️ एआई चाबी अमान्य है। कृपया वकील लॉगिन में जाकर सही चाबी दोबारा डालें।"
    except Exception as e:
        return f"⚠️ कनेक्शन में अस्थाई रुकावट: {str(e)}"

# =========================================================================
# 🌌 स्क्रीन 1: बैकग्राउंड में充 ब्लर लोगो और SKIP TIMER वाला टर्म्स पेज
# =========================================================================
if not st.session_state.terms_accepted:
    st.markdown("""
        <div style='position: relative; background-color: #1e293b; padding: 25px; border-radius: 15px; border: 3px solid #d97706; margin-top: 10px; color: #ffffff; overflow: hidden; max-width: 650px; margin-left: auto; margin-right: auto;'>
            <div style='position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                        background-image: url("https://postimg.cc"); 
                        background-size: cover; background-position: center; 
                        filter: blur(12px) brightness(0.2); opacity: 0.35; z-index: 1;'>
            </div>
            <div style='position: relative; z-index: 2; text-align: center;'>
                <div style='display: flex; justify-content: center; margin-bottom: 20px;'>
                    <img src='https://postimg.cc' style='width: 120px; height: 180px; object-fit: cover; border-radius: 10px; border: 1px solid #d97706;'>
                </div>
                <h1 style='color: #ffffff; margin: 5px 0; font-family: "Georgia", serif; font-weight: bold; letter-spacing: 2px; font-size: 38px;'>LEXA</h1>
                <p style='color: #f59e0b; margin: 0; font-family: "Dancing Script", cursive; font-size: 28px; font-weight: bold;'>by jaiswal</p>
                <hr style='border: 1px solid #334155; margin: 15px 0;'>
                <div style='text-align: left; padding: 5px; font-family: sans-serif; line-height: 1.5;'>
                    <h3 style='color: #f59e0b; margin-bottom: 5px; font-size: 18px;'>ℹ️ ऐप का मुख्य काम (Core Mission)</h3>
                    <p style='color: #cbd5e1; font-size: 13px; margin-top: 0;'>यह भारत का सबसे एडवांस एआई कानूनी सहायक प्लेटफॉर्म है। इसका मुख्य काम शिकायत/केस की कॉपियों का विश्लेषण करना, डिजिटल सबूतों और गवाहों के बयानों की आपस में फॉरेंसिक तुलना करके विरोधी पक्ष के झूठ को पकड़ना और उनके खिलाफ सुप्रीम कोर्ट के अचूक फैसलों के साथ मजबूत कानूनी याचिका और जवाब तैयार करना है।</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    timer_placeholder = st.empty()
    if not st.session_state.timer_complete:
        for seconds in range(5, 0, -1):
            timer_placeholder.markdown(f"<p style='text-align: center; color: #94a3b8; font-size:14px;'>⏳ आप {seconds} सेकंड बाद स्किप कर सकते हैं...</p>", unsafe_allow_html=True)
            time.sleep(1)
        st.session_state.timer_complete = True
        st.rerun()
    
    if st.session_state.timer_complete:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ I Agree & Enter LEXA", use_container_width=True):
                st.session_state.terms_accepted = True
                st.rerun()
        with col2:
            if st.button("⏩ SKIP (आगे बढ़ें)", use_container_width=True):
                st.session_state.terms_accepted = True
                st.rerun()

# =========================================================================
# 🛡️ स्क्रीन 2: मुख्य वर्किंग इंटरफेस (थ्री-पेज नेविगेशन)
# =========================================================================
else:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 10px;'>
            <div style='display: flex; justify-content: center; margin-bottom: 10px;'>
                <img src='https://postimg.cc' style='width: 75px; height: 110px; object-fit: cover; border-radius: 8px; border: 1px solid #d97706;'>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # रेस्पॉन्सिव नेविगेशन बटन्स
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        if st.button("📝 Petitioner File (प्रार्थी)", use_container_width=True, type="primary" if st.session_state.current_page == "Petitioner File" else "secondary"):
            st.session_state.current_page = "Petitioner File"
            st.rerun()
    with btn_col2:
        if st.button("🛡️ Respondent File (प्रतिवादी)", use_container_width=True, type="primary" if st.session_state.current_page == "Respondent File" else "secondary"):
            st.session_state.current_page = "Respondent File"
            st.rerun()
    with btn_col3:
        if st.button("💼 Advocates Manual Login (वकील लॉगिन)", use_container_width=True, type="primary" if st.session_state.current_page == "Advocates Manual Login" else "secondary"):
            st.session_state.current_page = "Advocates Manual Login"
            st.rerun()

    st.write("---")

    # 📑 भाग 1: PETITIONER FILE PAGE
    if st.session_state.current_page == "Petitioner File":
        st.markdown("<h2 style='text-align: center; font-size: 26px; color: #ffffff;'>PETITIONER FILE</h2>", unsafe_allow_html=True)
        col_p, col_r = st.columns(2)
        with col_p:
            p_info = st.text_area("RESPONDENT NAME, ADRESS", placeholder="प्रार्थी का नाम और पूरा पता दर्ज करें...", height=70)
        with col_r:
            r_info = st.text_area("PETITIONER NAME, ADRESS", placeholder="प्रतिवादी का नाम और पूरा पता दर्ज करें...", height=70)
        
        st.markdown("<h3 style='text-align: center; font-size: 20px; color: #ffffff; margin-top:20px;'>Evidence of Petitioner Against Respondent</h3>", unsafe_allow_html=True)
        
        # साक्ष्य इनपुट लॉजिक (अपलोड होते ही 3 पॉइंट्स मांगना)
        audio_file = st.file_uploader("AUDIO UPLOAD", type=["mp3", "wav", "m4a"])
        p_audio_pts = []
        if audio_file:
            st.info("✍️ ऑडियो साक्ष्य के 3 मुख्य विवरण दर्ज करें:")
            p_audio_pts.append(st.text_input("ऑडियो पॉइंट 1: इस रिकॉर्डिंग में क्या मुख्य बात साबित होती है?"))
            p_audio_pts.append(st.text_input("ऑडियो पॉइंट 2: यह बातचीत किस तारीख और समय की है?"))
            p_audio_pts.append(st.text_input("ऑडियो Point 3: बातचीत में शामिल व्यक्तियों के नाम:"))

        image_file = st.file_uploader("Image upload", type=["png", "jpg", "jpeg"])
        p_img_pts = []
        if image_file:
            st.info("✍️ इमेज साक्ष्य के 3 मुख्य विवरण दर्ज करें:")
            p_img_pts.append(st.text_input("इमेज पॉइंट 1: इस तस्वीर में क्या अवैध गतिविधि या घटना दिख रही है?"))
            p_img_pts.append(st.text_input("इमेज पॉइंट 2: यह फोटो किस स्थान पर खींची गई थी?"))
            p_img_pts.append(st.text_input("इमेज Point 3: फोटो का मुख्य साक्ष्य मूल्य क्या है?"))

        video_file = st.file_uploader("Witness video upload", type=["mp4", "mov"])
        p_vid_pts = []
        if video_file:
            st.info("✍️ वीडियो साक्ष्य के 3 मुख्य विवरण दर्ज करें:")
            p_vid_pts.append(st.text_input("वीडियो पॉइंट 1: इस वीडियो में गवाह या विरोधी क्या करता दिख रहा है?"))
            p_vid_pts.append(st.text_input("वीडियो पॉइंट 2: क्या यह वीडियो किसी सीसीटीवी या मोबाइल से बना है?"))
            p_vid_pts.append(st.text_input("वीडियो Point 3: वीडियो की प्रामाणिकता का विवरण:"))

        if st.button("⚖️ एआई फॉरेंसिक जांच एवं स्ट्रांगेस्ट याचिका तैयार करें", use_container_width=True):
            if p_info and r_info and st.session_state.gemini_key:
                with st.spinner("🧠 लाइव गूगल जेमिनी एआई प्रार्थी की स्ट्रांगेस्ट याचिका ड्राफ्ट कर रहा है..."):
                    pet_prompt = f"Draft strongest petition copy in Hindi for Court. Petitioner: {p_info}. Respondent: {r_info}. Audio data: {p_audio_pts}. Image data: {p_img_pts}. Video data: {p_vid_pts}. Include कड़क भारतीय कानूनी धाराएं (BNS)."
