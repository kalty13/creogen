import streamlit as st
import pandas as pd
import random
import io
import os

st.set_page_config(page_title="Creative Mixer", layout="wide")
st.title("🎬 Creative Content Mixer")

# ===== Pro Mode (уменьшенная кнопка + увеличенный тумблер) =====
st.markdown("""
<style>
.fake-pro-btn {
    display: inline-block;
    background: linear-gradient(90deg,#ffe066 60%,#ad69fa 100%);
    color: #232324;
    font-size: 1.06rem;
    font-weight: 800;
    border: none;
    border-radius: 15px;
    padding: 0.33em 1.3em;
    cursor: pointer;
    box-shadow: 0 4px 15px #ad69fa55;
    margin: 10px 0 2px 0;
    letter-spacing: 0.7px;
    text-shadow: 0 1px 4px #fff5, 0 1px 1px #ffe06650;
    user-select: none;
    animation: shine 2.1s linear infinite;
    transition: 
        transform 0.13s cubic-bezier(.4,2.4,.9,.8), 
        box-shadow 0.15s, 
        color 0.13s;
    outline: none;
}
.fake-pro-btn:hover {
    transform: scale(1.11) rotate(-2deg);
    box-shadow: 0 6px 20px #ffe06655, 0 0px 0 2px #ad69fa77;
    color: #ad69fa;
}
@keyframes shine {
    0% { box-shadow: 0 0 8px #ffe06644, 0 0 0 #ad69fa33;}
    50% { box-shadow: 0 0 16px #ad69fa99, 0 0 14px #ffe06633;}
    100% { box-shadow: 0 0 8px #ffe06644, 0 0 0 #ad69fa33;}
}
.big-toggle label[data-testid="stWidgetLabel"] {
    font-size: 1.42rem !important;
    font-weight: 800 !important;
    color: #ad69fa !important;
    letter-spacing: 0.5px;
}
.big-toggle div[data-testid="stToggle"] {
    zoom: 1.5;
}
</style>
<div class="fake-pro-btn" tabindex="0" title="Переведи тумблер ниже для активации!">🚀 Enable Pro Mode</div>
""", unsafe_allow_html=True)

if 'pro_mode_on' not in st.session_state:
    st.session_state['pro_mode_on'] = False

with st.container():
    st.markdown('<div class="big-toggle">', unsafe_allow_html=True)
    pro_mode = st.toggle("Pro Mode", value=st.session_state['pro_mode_on'], key="pro_toggle")
    st.markdown('</div>', unsafe_allow_html=True)
st.session_state['pro_mode_on'] = pro_mode

if st.session_state['pro_mode_on']:
    st.markdown("""
        <div style="
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(30,30,40,0.92); z-index: 9999; display: flex; align-items: center; justify-content: center;
        ">
            <div style="background: #232324; border: 3px solid #ffe066; border-radius: 18px; padding: 36px 48px; box-shadow: 0 8px 32px #0007; min-width: 370px; text-align: center;">
                <div style="font-size: 2.3rem; font-weight: bold; color: #ffe066;">🚀 Pro Mode</div>
                <div style="margin-top: 20px; font-size: 1.1rem; color: #fff;">
                    Хочешь пожизненный доступ к Pro-функциям и секретным фичам? 😉<br>
                    <span style="font-size: 1.45rem; font-weight: bold; color: #38ef7d;">0.003฿</span>
                    <div style="margin-top:12px; color:#ffe066; font-size: 1.15rem;">
                        Переведи на адрес:<br>
                        <span style="user-select: all; color: #fff; font-family: monospace;">
                            14H4r2phGv9mbK4XHDdDDR6JPjDbvDr6Zp
                        </span>
                    </div>
                    <div style="margin-top:10px; color:#ff6363; font-size: 0.99rem;">
                        После оплаты — напиши в <a href="https://t.me/kalty13" target="_blank" style="color:#ffe066;">Telegram</a>.<br>
                        Твой аккаунт будет разблокирован в течение 10 минут!
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    close_col = st.columns([6,1,6])[1]
    with close_col:
        if st.button("Закрыть окно Pro Mode", key="close_pro_btn"):
            st.session_state['pro_mode_on'] = False

# Sample CSV download
with st.expander("📎 Click to download a sample CSV"):
    with open("default_creatives.csv", "r") as f:
        st.download_button("Download Sample CSV", f.read(), file_name="sample_creative_template.csv")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file with Hooks, Characters, and Demos", type=["csv"])

# If no file uploaded, use default
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.info("✅ Loaded your uploaded file")
else:
    df = pd.read_csv("default_creatives.csv")
    st.warning("⚠️ No file uploaded. Using default_creatives.csv")

columns = df.columns.tolist()
hook_col = next((c for c in columns if "HOOK" in c.upper()), columns[0])
char_col = next((c for c in columns if "CHARACTER" in c.upper()), columns[1])
demo_col = next((c for c in columns if "DEMO" in c.upper()), columns[2])

df_filtered = df[[hook_col, char_col, demo_col]].copy()
df_filtered.columns = ['Hook', 'Character', 'Demo']

def extract_gender(text):
    if "woman" in text.lower():
        return "female"
    elif "man" in text.lower():
        return "male"
    else:
        return "unknown"

df_filtered["Gender"] = df_filtered["Character"].apply(extract_gender)

# Filters
st.sidebar.header("Filters")
gender_filter = st.sidebar.multiselect("Select Gender(s)", options=df_filtered["Gender"].unique(), default=df_filtered["Gender"].unique())
keyword = st.sidebar.text_input("Keyword search (any field)")

df_display = df_filtered[df_filtered["Gender"].isin(gender_filter)]
if keyword:
    df_display = df_display[df_display.apply(lambda row: keyword.lower() in row.to_string().lower(), axis=1)]

# Table
st.subheader("Filtered Components")
st.dataframe(df_display, use_container_width=True)

# Generate
st.markdown("---")
st.subheader("🔀 Generate Random Combinations")
num_creatives = st.slider("Number of combinations", 1, 20, 3)

generated_ideas = []
if st.button("Generate"):
    st.markdown("### Generated Creative Ideas")
    for _ in range(num_creatives):
        hook = random.choice(df_display["Hook"].tolist())
        character = random.choice(df_display["Character"].tolist())
        demo = random.choice(df_display["Demo"].tolist())

        idea = {
            "Hook": hook,
            "Character": character,
            "Demo": demo
        }
        generated_ideas.append(idea)

        st.markdown(f"""
**🎬 Creative Idea:**  
- **Hook:** {hook}  
- **Character:** {character}  
- **Demo:** {demo}  
---
""")

if generated_ideas:
    export_df = pd.DataFrame(generated_ideas)
    csv_data = export_df.to_csv(index=False).encode("utf-8")
    st.download_button("💾 Export Generated Ideas to CSV", csv_data, file_name="creative_ideas.csv")
