import streamlit as st
import requests

# --- फुल स्क्रीन लेआउट सेटिंग्स ---
st.set_page_config(page_title="LEXA", page_icon="⚖️", layout="wide")

# कर्सिव फ़ॉन्ट्स और स्टाइलिंग लोड करना
st.markdown("""
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Dancing+Script:wght@700&display=swap" rel="stylesheet">
    <style>.block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }</style>
""", unsafe_allow_html=True)

# सेशन स्टेट्स (डेटा को याद रखने के लिए)
if 'terms_accepted' not in st.session_state:
    st.session_state.terms_accepted = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Petitioner File"
if 'manual_lawyer_logged' not in st.session_state:
    st.session_state.manual_lawyer_logged = False
if 'gemini_key' not in st.session_state:
    st.session_state.gemini_key = ""

# लाइव एआई कॉलिंग फंक्शन
def call_gemini_ai(user_key, prompt_text):
    try:
        api_url = f"https://googleapis.com{user_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['candidates']['content']['parts']['text']
        else:
            return "⚠️ एआई चाबी (API Key) अमान्य है। कृपया वकील लॉगिन में सही चाबी डालें।"
    except Exception as e:
        return f"⚠️ कनेक्शन रुकावट: {str(e)}"

# =========================================================================
# 🌌 स्क्रीन 1: नया आलीशान ब्लर बैकग्राउंड और टाइमर वाला टर्म्स पेज
# =========================================================================
if not st.session_state.terms_accepted:
    st.markdown("""
        <div style='position: relative; background-color: #0f172a; padding: 25px; border-radius: 15px; border: 3px solid #d97706; text-align: center; max-width: 650px; margin: 0 auto;'>
            <div style='position: absolute; top:0; left:0; width:100%; height:100%; background-image: url("https://postimg.cc"); background-size: cover; filter: blur(12px) brightness(0.2); opacity: 0.3; z-index: 1;'></div>
            <div style='position: relative; z-index: 2;'>
                <img src='https://postimg.cc' style='width: 120px; height: 180px; object-fit: cover; border-radius: 10px; border: 1px solid #d97706; box-shadow: 0 4px 15px rgba(217,119,6,0.3);'>
                <h1 style='color: #ffffff; margin: 5px 0; font-family: "Georgia", serif; font-size: 38px;'>LEXA</h1>
                <p style='color: #f59e0b; margin: 0; font-family: "Dancing Script", cursive; font-size: 28px;'>by jaiswal</p>
                <hr style='border: 1px solid #334155; margin: 15px 0;'>
                <div style='text-align: left; font-size: 14px; color: #cbd5e1; line-height: 1.5;'>
                    <h4 style='color: #f59e0b; margin: 5px 0;'>ℹ️ मुख्य कार्य (Core Mission)</h4>
                    <p>शिकायत कॉपी और साक्ष्यों का विश्लेषण कर सुप्रीम कोर्ट के अचूक फैसलों के साथ मजबूत कानूनी याचिका और जवाब तैयार करना।</p>
                    <p style='font-weight: bold; margin-top: 10px; color: #e2e8f0;'>Owner Details: <span style='color: #f59e0b;'>JAISWAL</span></p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
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
    st.markdown("<div style='text-align: center; margin-bottom: 15px;'><img src='https://postimg.cc' style='width: 80px; height: 120px; object-fit: cover; border-radius: 8px; border: 1px solid #d97706;'></div>", unsafe_allow_html=True)

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
        if st.button("💼 Advocates Manual Login", use_container_width=True, type="primary" if st.session_state.current_page == "Advocates Manual Login" else "secondary"):
            st.session_state.current_page = "Advocates Manual Login"
            st.rerun()

    st.write("---")

    # 📑 1. PETITIONER FILE PAGE
    if st.session_state.current_page == "Petitioner File":
        st.markdown("<h2 style='text-align: center; text-decoration: underline; color: #ffffff;'>PETITIONER FILE</h2>", unsafe_allow_html=True)
        col_p, col_r = st.columns(2)
        with col_p:
            p_info = st.text_area("PETITIONER NAME, ADRESS", placeholder="प्रार्थी का नाम और पूरा पता दर्ज करें...", height=70)
        with col_r:
            r_info = st.text_area("RESPONDENT NAME, ADRESS", placeholder="प्रतिवादी का नाम और पूरा पता दर्ज करें...", height=70)

        st.markdown("<h3 style='text-align: center; color: #ffffff;'>Evidence of Petitioner Against Respondent</h3>", unsafe_allow_html=True)
        st.file_uploader("AUDIO UPLOAD (Mandatory Written Entry)", type=["mp3", "wav"])
        st.file_uploader("Image upload (Mandatory Written Entry)", type=["png", "jpg"])
        st.file_uploader("Witness video upload (Mandatory Written Entry)", type=["mp4"])
        
        p_p1 = st.text_input("बारीक लिखित विवरण दर्ज करें (पॉइंट 1):")
        
        if st.button("⚖️ एआई फॉरेंसिक जांच एवं स्ट्रांगेस्ट याचिका तैयार करें", use_container_width=True):
            if p_info and r_info and p_p1 and st.session_state.gemini_key:
                with st.spinner("🧠 लाइव गूगल जेमिनी एआई याचिका ड्राफ्ट कर रहा है..."):
                    prompt = f"Draft petition in Hindi for {p_info} against {r_info} based on: {p_p1}. Include BNS laws and Supreme Court Judgments."
                    st.write(call_gemini_ai(st.session_state.gemini_key, prompt))
            elif not st.session_state.gemini_key:
                st.error("🔑 कृपया पहले 'Advocates Manual Login' पेज पर अपनी Google API Key लॉक करें।")
            else:
                st.error("🛑 नाम, पता और लिखित ब्यौरा भरना अनिवार्य है!")

        st.markdown("<div style='text-align: center;'><a href='#' style='color: #cbd5e1; text-decoration: none;'>download the Petition copy here</a></div>", unsafe_allow_html=True)

    # 🛡️ 2. RESPONDENT FILE PAGE
    elif st.session_state.current_page == "Respondent File":
        st.markdown("<h2 style='text-align: center; text-decoration: underline; color: #ffffff;'>RESPONDENT FILE</h2>", unsafe_allow_html=True)
        col_r2, col_p2 = st.columns(2)
        with col_r2:
            r_info2 = st.text_area("RESPONDENT NAME, ADRESS", placeholder="प्रतिवादी का नाम और पूरा पता दर्ज करें...", height=70)
        with col_p2:
            p_info2 = st.text_area("PETITIONER NAME, ADRESS", placeholder="प्रार्थी का नाम और पूरा पता दर्ज करें...", height=70)

        st.markdown("<h3 style='text-align: center; color: #ffffff;'>Evidence Respondent Against Petitioner</h3>", unsafe_allow_html=True)
        pet_copy = st.file_uploader("PETITIONER'S COPY UPLOAD", type=["pdf", "jpg"])
        st.file_uploader("AUDIO UPLOAD", type=["mp3", "wav"])
        st.file_uploader("Image upload", type=["png", "jpg"])
        st.file_uploader("Witness video upload", type=["mp4"])
        
        r_p1 = st.text_input("बारीक लिखित विवरण दर्ज करें (पॉइंट 1):")

        if st.button("⚖️ एआई फॉरेंसिक जांच एवं स्ट्रांगेस्ट जवाबी प्रति तैयार करें", use_container_width=True):
            if r_info2 and p_info2 and r_p1 and pet_copy and st.session_state.gemini_key:
                with st.spinner("🧠 लाइव गूगल जेमिनी एआई जवाबी प्रति ड्राफ्ट कर रहा है..."):
                    prompt = f"Draft strongest reply in Hindi for Respondent: {r_info2} against Petitioner: {p_info2} based on: {r_p1}."
                    st.write(call_gemini_ai(st.session_state.gemini_key, prompt))
            elif not st.session_state.gemini_key:
                st.error("🔑 कृपया पहले 'Advocates Manual Login' पेज पर अपनी Google API Key लॉक करें।")
            else:
                st.error("🛑 नाम-पता, याचिका प्रति और लिखित ब्यौरा भरना अनिवार्य है!")

        st.markdown("<div style='text-align: center;'><a href='#' style='color: #cbd5e1; text-decoration: none;'>download the reply copy here</a></div>", unsafe_allow_html=True)

    # 💼 3. ADVOCATES MANUAL LOGIN
    elif st.session_state.current_page == "Advocates Manual Login":
        st.markdown("<h2 style='text-align: center; text-decoration: underline; color: #ffffff;'>ADVOCATES MANUAL LOGIN</h2>", unsafe_allow_html=True)

        if not st.session_state.manual_lawyer_logged:
            st.markdown("<div style='max-width: 450px; margin: 0 auto; padding: 15px; background-color: #1e293b; border-radius: 10px; border: 1px solid #d97706;'>", unsafe_allow_html=True)
            adv_id = st.text_input("बार काउंसिल आईडी / ईमेल दर्ज करें:")
            adv_pass = st.text_input("पासवर्ड दर्ज करें:", type="password")
