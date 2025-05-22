import streamlit as st
import pandas as pd
import random
import io

st.set_page_config(page_title="Creative Mixer", layout="wide")
st.title("🎬 Creative Content Mixer")

# 🔘 PRO MODE toggle
st.markdown("""
    <style>
    .pro-btn {
        display: inline-block;
        background: linear-gradient(90deg,#ffe066 0%,#ad69fa 100%);
        color: #232324;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        border-radius: 16px;
        padding: 0.5rem 1.2rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease-in-out;
        cursor: pointer;
        text-align: center;
        text-decoration: none;
    }
    .pro-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 0 12px rgba(173,105,250,0.6);
    }
    </style>
""", unsafe_allow_html=True)

if 'pro_mode' not in st.session_state:
    st.session_state.pro_mode = False

if st.button("✨ Enable PRO Mode", key="pro_button"):
    st.session_state.pro_mode = not st.session_state.pro_mode

if st.session_state.pro_mode:
    st.success("✅ PRO Mode Enabled! Advanced tools unlocked.")

# Sample CSV download
sample_csv = """HOOK,CHARACTER,PRODUCT DEMO
wait, so you're telling me i can understand my mind with just one app?,First-person POV selfie of young woman in oversized hoodie,A user opens the app and taps through a few questions
this is your sign to stop ignoring your feelings,First-person POV selfie of young man at a desk,A user types “Feeling stressed” into the app
"""

with st.expander("📎 Click to download a sample CSV"):
    st.download_button("Download Sample CSV", sample_csv, file_name="sample_creative_template.csv")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file with Hooks, Characters, and Demos", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

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

    # Sidebar filters
    st.sidebar.header("Filters")
    gender_filter = st.sidebar.multiselect("Select Gender(s)", options=df_filtered["Gender"].unique(), default=df_filtered["Gender"].unique())
    keyword = st.sidebar.text_input("Keyword search (any field)")

    df_display = df_filtered[df_filtered["Gender"].isin(gender_filter)]
    if keyword:
        df_display = df_display[df_display.apply(lambda row: keyword.lower() in row.to_string().lower(), axis=1)]

    # Show filtered data
    st.subheader("Filtered Components")
    st.dataframe(df_display, use_container_width=True)

    # Generation block
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

    # Export
    if generated_ideas:
        export_df = pd.DataFrame(generated_ideas)
        csv_data = export_df.to_csv(index=False).encode("utf-8")
        st.download_button("💾 Export Generated Ideas to CSV", csv_data, file_name="creative_ideas.csv")
