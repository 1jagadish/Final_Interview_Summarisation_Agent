import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8001"

st.set_page_config(layout="wide")

st.title("Interview Summarization Agent")

# -----------------------------
# 🔹 Sidebar
# -----------------------------
st.sidebar.header("Repository")

try:
    res = requests.get(f"{BASE_URL}/transcripts")
    res.raise_for_status()
    files = res.json().get("files", [])
except Exception:
    st.error("❌ Failed to fetch transcripts from backend")
    files = []

selected = st.sidebar.selectbox("Select Transcript", files)

# -----------------------------
# 🔹 PREVIEW (NO AI CALL)
# -----------------------------
if selected:
    try:
        preview_res = requests.get(
            f"{BASE_URL}/preview",
            params={"file_name": selected}
        )
        preview_res.raise_for_status()
        preview_data = preview_res.json()
    except Exception:
        st.error("❌ Failed to load transcript preview")
        preview_data = {}

    col1, col2 = st.columns(2)

    # -----------------------------
    # LEFT SIDE (RAW TRANSCRIPT)
    # -----------------------------
    with col1:
        st.subheader("Raw Transcript")

        meta = preview_data.get("meta", {})
        st.write(f"**Candidate:** {meta.get('name', 'N/A')}")
        st.write(f"**Role:** {meta.get('role', 'N/A')}")
        st.write(f"**Date:** {meta.get('date', 'N/A')}")

        st.text_area(
            "Transcript",
            preview_data.get("transcript", ""),
            height=350
        )

    # -----------------------------
    # RIGHT SIDE (ANALYSIS)
    # -----------------------------
    with col2:
        st.subheader("Agent Output")

        if st.button("✨ Analyze Candidate"):

            try:
                response = requests.get(
                    f"{BASE_URL}/analyze",
                    params={"file_name": selected}
                )
                response.raise_for_status()
                data = response.json()
            except Exception:
                st.error("❌ Analysis failed. Check backend.")
                data = {}

            st.success("Analysis Complete")

            # 🎯 Recommendation
            st.markdown(
                f"### 🎯 Recommendation: `{data.get('recommendation', 'Unknown')}`"
            )

            # 📄 Summary
            st.subheader("Executive Summary")
            st.write(data.get("summary", ""))

            # 💪 Strengths
            st.subheader("Key Strengths")
            strengths = data.get("strengths", [])
            if strengths:
                for point in strengths:
                    st.success(f"• {point}")
            else:
                st.info("No strengths identified")

            # ⚠️ Improvements
            st.subheader("Areas for Improvement")
            improvements = data.get("improvements", [])
            if improvements:
                for point in improvements:
                    st.warning(f"• {point}")
            else:
                st.info("No improvements identified")

# -----------------------------
# 📊 REPORTING SECTION
# -----------------------------
st.markdown("---")
st.subheader("📊 Reporting")

st.write("Save all generated metrics and historical analyses directly to Excel.")

download_url = f"{BASE_URL}/download"

st.markdown(
    f"""
    <a href="{download_url}" target="_blank">
        <button style="
            background-color:#4CAF50;
            color:white;
            padding:12px 20px;
            border:none;
            border-radius:8px;
            font-size:16px;
            cursor:pointer;">
            📊 Download All Analyses (Excel)
        </button>
    </a>
    """,
    unsafe_allow_html=True
)