import streamlit as st

st.set_page_config(
    page_title="Nexus HTML Test",
    layout="wide",
)

st.title("Nexus HTML Rendering Test")

st.html(
    """
    <div style="
        background: #0F151D;
        border: 1px solid #8B5CF6;
        border-radius: 12px;
        padding: 30px;
        color: white;
        font-size: 24px;
    ">
        HTML IS WORKING
    </div>
    """
)

st.html(
    """
    <style>
        .test-card {
            background: #0F151D;
            border: 1px solid #202A36;
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
        }

        .test-title {
            color: #8B5CF6;
            font-weight: 700;
            font-size: 20px;
        }

        .test-description {
            color: #8995A5;
            margin-top: 10px;
        }
    </style>

    <div class="test-card">
        <div class="test-title">
            FINDING 1
        </div>

        <div class="test-description">
            This is a test finding.
        </div>
    </div>
    """
)