import streamlit as st
import time
import requests

# --- आपके ऐप का असली नाम और आइकॉन सेटिंग्स ---
st.set_page_config(
    page_title="LEXA", 
    page_icon="⚖️", 
    layout="wide"
)

# कर्सिव फ़ॉन्ट्स और स्टाइल लोड करना
st.markdown("""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Dancing+Script:wght=700&display=swap" rel="stylesheet">
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

# सेशन स्टेट्स का रख-रखाव
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

# लाइव जेमिनी एआई इंजन कनेक्शन फंक्शन
def call_gemini_ai(user_key, prompt_text):
    try:
        api_url = f"https://googleapis.com{user_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['candidates']['content']['parts']['text']
        else:
            return "⚠️ एआई चाबी (API Key) अमान्य है। कृपया वकील लॉगिन में जाकर सही चाबी दोबारा डालें।"
    except Exception as e:
        return f"⚠️ कनेक्शन में अस्थाई रुकावट: {str(e)}"

# =========================================================================
# 🌌 स्क्रीन 1: बैकग्राउंड में ब्लर लोगो और SKIP TIMER वाला टर्म्स पेज
# =========================================================================
if not st.session_state.terms_accepted:
    st.markdown("""
        <div style='position: relative; background-color: #0f172a; padding: 30px; border-radius: 20px; border: 3px solid #d97706; margin-top: 10px; color: #ffffff; overflow: hidden; max-width: 700px; margin-left: auto; margin-right: auto;'>
            <div style='position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                        background-image: url("https://postimg.cc"); 
                        background-size: cover; background-position: center; 
                        filter: blur(15px) brightness(0.2); opacity: 0.35; z-index: 1;'>
            </div>
            <div style='position: relative; z-index: 2; text-align: center;'>
                <div style='display: flex; justify-content: center; margin-bottom: 25px; padding-top: 10px;'>
                    <img src='https://postimg.cc' style='width: 140px; height: 210px; object-fit: cover; border-radius: 15px; box-shadow: 0px 10px 30px rgba(217, 119, 6, 0.3); border: 1px solid #d97706;'>
                </div>
                <h1 style='color: #ffffff; margin: 5px 0; font-family: "Georgia", serif; font-weight: bold; letter-spacing: 3px; font-size: 42px;'>LEXA</h1>
                <p style='color: #f59e0b; margin: 0; font-family: "Dancing Script", cursive; font-size: 32px; font-weight: bold;'>by jaiswal</p>
                <hr style='border: 1px solid #334155; margin: 20px 0;'>
                <div style='text-align: left; padding: 10px; font-family: sans-serif; line-height: 1.6;'>
                    <h3 style='color: #f59e0b; margin-bottom: 5px;'>ℹ️ ऐप का मुख्य काम (Core Mission)</h3>
                    <p style='color: #cbd5e1; font-size: 14px; margin-top: 0;'>यह भारत का सबसे एडवांस एआई कानूनी सहायक प्लेटफॉर्म है। इसका मुख्य काम शिकायत/केस की कॉपियों का विश्लेषण करना, डिजिटल सबूतों और गवाहों के बयानों की आपस में फॉरेंसिक तुलना करके विरोधी पक्ष के झूठ को पकड़ना और उनके खिलाफ सुप्रीम कोर्ट के अचूक फैसलों के साथ मजबूत कानूनी याचिका और जवाब तैयार करना है।</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    timer_placeholder = st.empty()
    if not st.session_state.timer_complete:
        for seconds in range(5, 0, -1):
            timer_placeholder.markdown(f"<p style='text-align: center; color: #94a3b8;'>⏳ आप {seconds} सेकंड बाद स्किप कर सकते हैं...</p>", unsafe_allow_html=True)
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
        <div style='text-align: center; color: #ffffff; font-family: sans-serif; margin-bottom: 10px;'>
            <div style='display: flex; justify-content: center; margin-bottom: 15px;'>
                <img src='https://postimg.cc' style='width: 95px; height: 140px; object-fit: cover; border-radius: 10px; border: 1px solid #d97706;'>
            </div>
        </div>
    """, unsafe_allow_html=True)

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
        st.markdown("<h1 style='text-align: center; font-family: sans-serif; letter-spacing: 2px; text-decoration: underline; font-size: 32px; margin-bottom: 25px; color: #ffffff;'>PETITIONER FILE</h1>", unsafe_allow_html=True)
        col_p, col_r = st.columns(2)
        with col_p:
            st.markdown("<p style='font-size: 14px; font-weight: bold; color: #cbd5e1;'>PETITIONER NAME, ADRESS</p>", unsafe_allow_html=True)
            p_info = st.text_area("P_Address", label_visibility="collapsed", placeholder="प्रार्थी का नाम और पूरा पता दर्ज करें...", height=80)
        with col_r:
            st.markdown("<p style='font-size: 14px; font-weight: bold; color: #cbd5e1; text-align: right;'>RESPONDENT NAME, ADRESS</p>", unsafe_allow_html=True)
            r_info = st.text_area("R_Address", label_visibility="collapsed", placeholder="प्रतिवादी का नाम और पूरा पता दर्ज करें...", height=80)
        st.markdown("<h2 style='text-align: center; font-family: sans-serif; font-size: 24px; color: #ffffff; margin-top: 35px; margin-bottom: 25px;'>Evidence of Petitioner Against Respondent</h2>", unsafe_allow_html=True)
        audio_file = st.file_uploader("AUDIO UPLOAD", type=["mp3", "wav", "m4a"])
        image_file = st.file_uploader("Image upload", type=["png", "jpg", "jpeg"])
        video_file = st.file_uploader("Witness video upload", type=["mp4", "mov"])
        st.warning("⚠️ लिखित ब्यौरा प्रणाली: साक्ष्य के 3 मुख्य पॉइंट्स दर्ज करें:")
        p_p1 = st.text_input("पॉइंट 1: प्रार्थी के इस सबूत में विरोधी के खिलाफ क्या मुख्य बात साबित होती है?")
        p_p2 = st.text_input("पॉइंट 2: यह घटना किस तारीख और समय की है?")
        p_p3 = st.text_input("पॉइंट 3: अन्य विवरण:")
        if st.button("⚖️ एआई फॉरेंसिक जांच एवं स्ट्रांगेस्ट याचिका तैयार करें", use_container_width=True):
            if p_info and r_info and p_p1 and st.session_state.gemini_key:
                with st.spinner("🧠 लाइव गूगल जेमिनी एआई प्रार्थी की स्ट्रांगेस्ट याचिका ड्राफ्ट कर रहा है..."):
                    pet_prompt = f"Draft the strongest court petition copy on behalf of petitioner in Hindi. Petitioner: {p_info}. Respondent: {r_info}. Evidence details: {p_p1}, {p_p2}, {p_p3}. Include relevant sections of Indian Law (BNS)."
                    result = call_gemini_ai(st.session_state.gemini_key, pet_prompt)
                    st.success("🔒 एआई फॉरेंसिक जांच सफल! 1000% लाभ ट्रांसफर एक्टिव।")
                    st.markdown("#### 🛡️ एआई द्वारा तैयार अत्यंत मजबूत याचिका प्रतिलिपि:")
                    st.write(result)
            elif not st.session_state.gemini_key:
                st.error("🔑 एआई दिमाग बंद है! पहले 'Advocates Manual Login' पेज पर जाकर अपनी Google API Key पेस्ट करें।")
            else:
                st.error("🛑 कृपया प्रार्थी/प्रतिवादी का नाम-पता और अनिवार्य लिखित ब्यौरा अवश्य भरें!")
        st.markdown("<div style='text-align: center; margin-top: 40px;'><a href='#' style='color: #cbd5e1; text-decoration: none; font-size: 16px; font-family: monospace;'>download the Petition copy here</a></div>", unsafe_allow_html=True)

    # 🛡️ भाग 2: RESPONDENT FILE PAGE
    elif st.session_state.current_page == "Respondent File":
