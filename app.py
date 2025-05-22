import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Creative Mixer", layout="wide")
st.title("🎬 Creative Content Mixer")

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

    st.sidebar.header("Filters")
    gender_filter = st.sidebar.multiselect("Select Gender(s)", options=df_filtered["Gender"].unique(), default=df_filtered["Gender"].unique())
    keyword = st.sidebar.text_input("Keyword search (any field)")

    df_display = df_filtered[df_filtered["Gender"].isin(gender_filter)]
    if keyword:
        df_display = df_display[df_display.apply(lambda row: keyword.lower() in row.to_string().lower(), axis=1)]

    st.subheader("Filtered Components")
    st.dataframe(df_display, use_container_width=True)

    st.markdown("---")
    st.subheader("🔀 Generate Random Combinations")
    num_creatives = st.slider("Number of combinations", 1, 10, 3)

    if st.button("Generate"):
        st.markdown("### Generated Creative Ideas")
        for _ in range(num_creatives):
            hook = random.choice(df_display["Hook"].tolist())
            character = random.choice(df_display["Character"].tolist())
            demo = random.choice(df_display["Demo"].tolist())

            st.markdown(f"""
            **🎬 Creative Idea:**
            - **Hook:** {hook}  
            - **Character:** {character}  
            - **Demo:** {demo}  
            ---
            """)
