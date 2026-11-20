import streamlit as st

# set up the webpage
st.set_page_config(
    page_title="AI Policy Analyzer",
    page_icon="🔎",
    layout="wide"
)

# custom webpage styling
st.markdown("""
<style>
    .stApp {
        background-color: #F3F6FA;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
    }

    .hero {
        background-color: #101E35;
        padding: 35px;
        border-radius: 15px;
        margin-bottom: 30px;
    }

    .hero h1 {
        color: white;
        font-size: 38px;
        margin-bottom: 10px;
    }

    .hero p {
        color: #C5D2E5;
        font-size: 17px;
    }

    .section-title {
        color: #172B49;
        font-size: 23px;
        font-weight: bold;
        margin-bottom: 8px;
    }

    .stButton button {
        background-color: #0F766E;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
    }

    .stButton button:hover {
        background-color: #115E59;
        color: white;
    }

    .footer {
        text-align: center;
        color: #64748B;
        font-size: 13px;
        margin-top: 50px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)


# main heading
st.markdown("""
<div class="hero">
    <h1>🔎 AI Policy Analyzer</h1>
    <p>Know what you're agreeing to before accepting the fine print.</p>
</div>
""", unsafe_allow_html=True)


# upload section
st.markdown(
    '<p class="section-title">01. Upload Your Policy</p>',
    unsafe_allow_html=True
)

st.write("Upload a PDF document or paste its text below.")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

st.markdown("**Or paste your policy text:**")

policy_text = st.text_area(
    "Policy Text",
    placeholder="Paste your Terms of Service or Privacy Policy here...",
    height=220,
    label_visibility="collapsed"
)


# analyze button
st.divider()

if st.button("Analyze Policy", type="primary", use_container_width=True):

    if uploaded_file is None and not policy_text.strip():
        st.error("Please upload a PDF or paste policy text.")

    else:
        st.success("Your document has been received!")

        st.info(
            "Your document is ready. The AI analysis "
            "connection will be added when the backend is ready."
        )


# results display function
def display_results(analysis, report):

    st.divider()

    st.markdown(
        '<p class="section-title">02. Policy Analysis Results</p>',
        unsafe_allow_html=True
    )

    # document information
    st.subheader(analysis.document_type)

    if analysis.company_name:
        st.caption("Company: " + analysis.company_name)

    # risk level
    st.subheader("Overall Risk Level")

    if analysis.risk_level == "high":
        st.error("HIGH RISK")

    elif analysis.risk_level == "medium":
        st.warning("MEDIUM RISK")

    else:
        st.success("LOW RISK")

    # summary
    st.subheader("Overall Summary")
    st.write(analysis.overall_summary)

    # key takeaways
    st.subheader("Key Takeaways")

    for takeaway in analysis.key_takeaways:
        st.markdown("- " + takeaway)

    # flagged clauses
    st.subheader("Flagged Clauses")

    if analysis.flagged_clauses:

        for clause in analysis.flagged_clauses:

            with st.expander(clause.clause_type):

                st.write("Severity:", clause.severity.upper())

                st.write("Document Excerpt:")
                st.write(clause.excerpt)

                st.write("Why This Matters:")
                st.write(clause.why_flagged)

    else:
        st.write("No concerning clauses were identified.")

    # data collected
    st.subheader("Data Collected")

    if analysis.data_collected:

        for item in analysis.data_collected:
            st.markdown("- " + item)

    else:
        st.write("No data collection information was identified.")

    # download the report
    st.subheader("Download Yoru Report")

    st.download_button(
        label = "Download Analyss Report",
        data = report,
        file_name = "policy_analysis.md",
        mime = "text/markdown"
    )


# footer
st.markdown("""
<div class="footer">
    AI Policy Analyzer | Helping consumers understand agreements.
    <br>
    This tool provides general information and does not replace legal advice.
</div>
""", unsafe_allow_html=True)
