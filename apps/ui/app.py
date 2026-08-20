import html

import requests
import streamlit as st

from config import API_BASE_URL


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Nexus AI",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# HTML RENDERER
# =========================================================

def render_html(content: str) -> None:
    st.html(content)


# =========================================================
# GLOBAL CSS
# =========================================================

render_html(
    """
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    .stApp {
        background: #090D12;
        color: #E6EDF3;
    }

    .block-container {
        max-width: 1380px;
        padding-top: 2.5rem;
        padding-bottom: 5rem;
    }

    footer {
        visibility: hidden;
    }

    [data-testid="stHeader"] {
        background: #090D12;
    }

    [data-testid="stToolbar"] {
        background: transparent;
    }

    hr {
        border-color: #1D2630 !important;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background: #0C1118;
        border-right: 1px solid #1E2732;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    .sidebar-brand {
        color: #F4F7FA;
        font-size: 1.35rem;
        font-weight: 750;
        letter-spacing: -0.035em;
    }

    .sidebar-mark {
        color: #8B5CF6;
    }

    .sidebar-subtitle {
        color: #758193;
        font-size: 0.78rem;
        line-height: 1.45;
        margin-top: 0.3rem;
        margin-bottom: 1.6rem;
    }

    .sidebar-section {
        color: #657286;
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-top: 1.7rem;
        margin-bottom: 0.7rem;
    }


    /* =====================================================
       HERO
       ===================================================== */

    .hero {
        text-align: center;
        max-width: 900px;
        margin: 2.5rem auto 2.8rem auto;
    }

    .hero-mark {
        color: #8B5CF6;
        font-size: 1.15rem;
        margin-right: 0.35rem;
    }

    .hero-title {
        color: #F4F7FA;
        font-size: 3.1rem;
        font-weight: 780;
        letter-spacing: -0.065em;
        line-height: 1.05;
        margin: 0;
    }

    .hero-title-accent {
        color: #8B5CF6;
    }

    .hero-subtitle {
        color: #8A96A5;
        font-size: 1.02rem;
        line-height: 1.65;
        max-width: 720px;
        margin: 1rem auto 0 auto;
    }

    .hero-note {
        display: inline-block;
        margin-top: 1.2rem;
        padding: 0.4rem 0.75rem;
        border: 1px solid #252F3B;
        border-radius: 999px;
        color: #788597;
        background: #0D131A;
        font-size: 0.7rem;
        letter-spacing: 0.04em;
    }


    /* =====================================================
       WORKSPACE
       ===================================================== */

    .workspace {
        max-width: 950px;
        margin: 0 auto;
    }

    .workspace-label {
        color: #F4F7FA;
        font-size: 0.78rem;
        font-weight: 720;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.65rem;
    }

    .workspace-description {
        color: #748092;
        font-size: 0.83rem;
        line-height: 1.5;
        margin-bottom: 0.9rem;
    }


    /* =====================================================
       EXAMPLES
       ===================================================== */

    .examples-label {
        color: #697687;
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 1.8rem;
        margin-bottom: 0.65rem;
    }

    .example-card {
        background: #0E141B;
        border: 1px solid #202A36;
        border-radius: 11px;
        padding: 0.85rem 1rem;
        min-height: 70px;
    }

    .example-category {
        color: #8B5CF6;
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
    }

    .example-question {
        color: #C6CED8;
        font-size: 0.78rem;
        line-height: 1.4;
    }


    /* =====================================================
       PRODUCT PRINCIPLES
       ===================================================== */

    .principles {
        max-width: 950px;
        margin: 3.5rem auto 0 auto;
        padding-top: 1.8rem;
        border-top: 1px solid #1D2630;
    }

    .principle {
        text-align: center;
        padding: 0 1.2rem;
    }

    .principle-icon {
        color: #8B5CF6;
        font-size: 1rem;
        margin-bottom: 0.55rem;
    }

    .principle-title {
        color: #DDE3EA;
        font-size: 0.78rem;
        font-weight: 680;
        margin-bottom: 0.3rem;
    }

    .principle-description {
        color: #687587;
        font-size: 0.7rem;
        line-height: 1.45;
    }


    /* =====================================================
       INPUT
       ===================================================== */

    textarea {
        background: #0F151D !important;
        color: #E6EDF3 !important;
        border: 1px solid #273241 !important;
        border-radius: 13px !important;
        box-shadow: none !important;
        font-size: 0.95rem !important;
    }

    textarea:focus {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 1px #8B5CF6 !important;
    }


    /* =====================================================
       SELECT
       ===================================================== */

    div[data-baseweb="select"] > div {
        background: #0F151D !important;
        border: 1px solid #273241 !important;
        border-radius: 10px !important;
    }

    label {
        color: #8995A5 !important;
        font-size: 0.76rem !important;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    button[kind="primary"] {
        background: #7C3AED !important;
        border: 1px solid #8B5CF6 !important;
        color: #FFFFFF !important;
        font-weight: 680 !important;
        border-radius: 10px !important;
        min-height: 43px;
    }

    button[kind="primary"]:hover {
        background: #8B5CF6 !important;
        border-color: #A78BFA !important;
    }

    button {
        border-radius: 10px !important;
    }


    /* =====================================================
       RESULT CARDS
       ===================================================== */

    .section-label {
        color: #F4F7FA;
        font-size: 1.05rem;
        font-weight: 680;
        margin-bottom: 0.4rem;
    }

    .section-description {
        color: #7F8B9A;
        font-size: 0.86rem;
        line-height: 1.55;
        max-width: 850px;
        margin-bottom: 1.1rem;
    }

    .nexus-card {
        background: #0F151D;
        border: 1px solid #202A36;
        border-radius: 14px;
        padding: 1.25rem;
    }

    .card-label {
        color: #718092;
        font-size: 0.7rem;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.45rem;
    }


    /* =====================================================
       CLAIM
       ===================================================== */

    .claim-card {
        background: #15120D;
        border: 1px solid #4C3A1D;
        border-radius: 14px;
        padding: 1.35rem;
    }

    .claim-warning {
        color: #F0B84B;
        font-size: 0.72rem;
        font-weight: 750;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    .claim-number {
        color: #F4F7FA;
        font-size: 1.8rem;
        font-weight: 750;
        line-height: 1.1;
    }

    .claim-caption {
        color: #758193;
        font-size: 0.7rem;
        font-weight: 650;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
    }

    .claim-explanation {
        color: #A59A87;
        font-size: 0.82rem;
        line-height: 1.5;
        margin-top: 1rem;
        max-width: 850px;
    }


    /* =====================================================
       ROOT CAUSE
       ===================================================== */

    .root-card {
        background: #0E1814;
        border: 1px solid #254638;
        border-radius: 14px;
        padding: 1.25rem;
        margin-bottom: 0.8rem;
    }

    .root-index {
        color: #75D5A4;
        font-size: 0.7rem;
        font-weight: 750;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .root-title {
        color: #F1F6F3;
        font-size: 1.05rem;
        font-weight: 700;
        margin-top: 0.3rem;
        margin-bottom: 0.55rem;
    }

    .root-description {
        color: #B6C2BD;
        font-size: 0.88rem;
        line-height: 1.55;
    }

    .root-meta {
        color: #74847D;
        font-size: 0.76rem;
        margin-top: 0.85rem;
    }


    /* =====================================================
       FINDINGS
       ===================================================== */

    .finding-card {
        background: #0E141B;
        border: 1px solid #202A36;
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.65rem;
    }

    .finding-number {
        color: #8B5CF6;
        font-size: 0.72rem;
        font-weight: 750;
        letter-spacing: 0.08em;
    }

    .finding-title {
        color: #E9EEF4;
        font-size: 0.95rem;
        font-weight: 650;
        margin-top: 0.2rem;
    }

    .finding-description {
        color: #8995A5;
        font-size: 0.83rem;
        line-height: 1.5;
        margin-top: 0.4rem;
    }


    /* =====================================================
       TIMELINE
       ===================================================== */

    .timeline {
        display: flex;
        gap: 0.45rem;
        width: 100%;
        margin: 1.2rem 0 1.6rem 0;
    }

    .timeline-item {
        flex: 1;
        text-align: center;
        padding: 0.7rem 0.3rem;
        border: 1px solid #26313D;
        border-radius: 9px;
        background: #0E141B;
        color: #8A96A5;
        font-size: 0.67rem;
        line-height: 1.4;
    }

    .timeline-complete {
        border-color: #254638;
        background: #0D1713;
        color: #7ED6A9;
    }


    /* =====================================================
       METRICS
       ===================================================== */

    [data-testid="stMetric"] {
        background: #0F151D;
        border: 1px solid #202A36;
        border-radius: 12px;
        padding: 0.9rem;
    }

    [data-testid="stMetricLabel"] {
        color: #778496 !important;
    }

    [data-testid="stMetricValue"] {
        color: #F4F7FA !important;
    }

    </style>
    """
)


# =========================================================
# SESSION STATE
# =========================================================

if "investigation" not in st.session_state:
    st.session_state.investigation = None

if "question_input" not in st.session_state:
    st.session_state.question_input = ""


# =========================================================
# API FUNCTIONS
# =========================================================

def create_investigation(
    question: str,
    priority: str,
) -> dict:

    response = requests.post(
        f"{API_BASE_URL}/investigations",
        json={
            "question": question,
            "priority": priority,
        },
        timeout=300,
    )

    response.raise_for_status()

    return response.json()


def get_investigation(
    investigation_id: str,
) -> dict:

    response = requests.get(
        f"{API_BASE_URL}/investigations/{investigation_id}",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()

def list_investigations(
    limit: int = 8,
) -> list[dict]:

    response = requests.get(
        f"{API_BASE_URL}/investigations",
        params={"limit": limit},
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# HELPERS
# =========================================================

def format_confidence(value) -> str:

    if value is None:
        return "N/A"

    try:
        return f"{float(value):.0%}"

    except (TypeError, ValueError):
        return "N/A"


def render_timeline() -> None:

    stages = [
        "Planning",
        "Analysis",
        "Evidence",
        "Synthesis",
        "Validation",
        "Root Cause",
        "Report",
    ]

    items = ""

    for stage in stages:

        items += f"""
        <div class="timeline-item timeline-complete">
            ✓<br>{html.escape(stage)}
        </div>
        """

    render_html(
        f"""
        <div class="timeline">
            {items}
        </div>
        """
    )


def set_example_question(question: str) -> None:

    st.session_state.question_input = question


# =========================================================
# SIDEBAR
# =========================================================

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    render_html(
        """
        <div class="sidebar-brand">
            <span class="sidebar-mark">◆</span> NEXUS AI
        </div>

        <div class="sidebar-subtitle">
            Cognitive Investigation Platform
        </div>
        """
    )

    # -----------------------------------------------------
    # NEW INVESTIGATION
    # -----------------------------------------------------

    if st.button(
        "＋  New Investigation",
        use_container_width=True,
        type="primary",
    ):

        st.session_state.investigation = None
        st.session_state.question_input = ""

        st.rerun()


    # -----------------------------------------------------
    # RECENT INVESTIGATIONS
    # -----------------------------------------------------

    render_html(
        """
        <div class="sidebar-section">
            Recent Investigations
        </div>
        """
    )

    try:

        investigations = list_investigations(
            limit=8
        )

        if not investigations:

            render_html(
                """
                <div
                    style="
                        color:#687587;
                        font-size:0.76rem;
                        line-height:1.5;
                        padding:0.4rem 0;
                    "
                >
                    No investigations yet.
                </div>
                """
            )

        else:

            for item in investigations:

                investigation_id = item.get("id")

                question = str(
                    item.get(
                        "question",
                        "Untitled investigation",
                    )
                )

                status_value = str(
                    item.get(
                        "status",
                        "unknown",
                    )
                ).lower()

                priority_value = str(
                    item.get(
                        "priority",
                        "medium",
                    )
                ).lower()

                confidence = item.get(
                    "confidence_score"
                )


                # Shorten question for sidebar
                if len(question) > 52:

                    display_question = (
                        question[:52].rstrip()
                        + "..."
                    )

                else:

                    display_question = question


                safe_question = html.escape(
                    display_question
                )


                # Status
                if status_value == "completed":

                    status_label = "COMPLETED"
                    status_color = "#7ED6A9"

                elif status_value == "pending":

                    status_label = "PENDING"
                    status_color = "#F0B84B"

                elif status_value == "failed":

                    status_label = "FAILED"
                    status_color = "#F87171"

                else:

                    status_label = status_value.upper()
                    status_color = "#8A96A5"


                # Confidence
                if confidence is not None:

                    confidence_label = (
                        format_confidence(confidence)
                    )

                else:

                    confidence_label = "—"


                # -------------------------------------------------
                # Investigation preview
                # -------------------------------------------------

                render_html(
                    f"""
                    <div
                        style="
                            padding:0.65rem 0.15rem 0.35rem 0.15rem;
                        "
                    >

                        <div
                            style="
                                color:#C6CED8;
                                font-size:0.76rem;
                                line-height:1.4;
                                margin-bottom:0.35rem;
                            "
                        >
                            {safe_question}
                        </div>

                        <div
                            style="
                                display:flex;
                                align-items:center;
                                gap:0.4rem;
                                font-size:0.62rem;
                                letter-spacing:0.04em;
                            "
                        >

                            <span
                                style="
                                    color:{status_color};
                                    font-weight:700;
                                "
                            >
                                {status_label}
                            </span>

                            <span style="color:#4E5A68;">
                                •
                            </span>

                            <span
                                style="
                                    color:#707D8E;
                                    text-transform:uppercase;
                                "
                            >
                                {html.escape(priority_value)}
                            </span>

                            <span style="color:#4E5A68;">
                                •
                            </span>

                            <span style="color:#707D8E;">
                                {confidence_label}
                            </span>

                        </div>

                    </div>
                    """
                )


                # -------------------------------------------------
                # Open investigation button
                # -------------------------------------------------

                if st.button(
                    "Open",
                    key=f"open_{investigation_id}",
                    use_container_width=True,
                ):

                    try:

                        loaded_investigation = (
                            get_investigation(
                                str(investigation_id)
                            )
                        )

                        st.session_state.investigation = (
                            loaded_investigation
                        )

                        st.rerun()

                    except requests.RequestException as exc:

                        st.error(
                            f"Unable to load investigation: {exc}"
                        )


    except requests.RequestException:

        render_html(
            """
            <div
                style="
                    color:#F87171;
                    font-size:0.74rem;
                    line-height:1.5;
                "
            >
                Unable to load investigation history.
            </div>
            """
        )


    # -----------------------------------------------------
    # SYSTEM
    # -----------------------------------------------------

    render_html(
        """
        <div class="sidebar-section">
            System
        </div>
        """
    )

    try:

        health = requests.get(
            f"{API_BASE_URL}/health",
            timeout=5,
        )

        if health.ok:

            st.success("API Connected")

        else:

            st.error("API Unavailable")

    except requests.RequestException:

        st.error("API Unavailable")

    st.caption(
        f"Backend: `{API_BASE_URL}`"
    )

# =========================================================
# LANDING / NEW INVESTIGATION
# =========================================================

if st.session_state.investigation is None:

    render_html(
        """
        <div class="hero">

            <div class="hero-title">
                <span class="hero-mark">◆</span>
                NEXUS <span class="hero-title-accent">AI</span>
            </div>

            <div class="hero-subtitle">
                Evidence-driven investigation and root-cause reasoning.
                Ask a business question and let Nexus validate the claim,
                investigate the evidence, and identify the strongest
                supported drivers.
            </div>

            <div class="hero-note">
                Evidence first · Causality aware · Explainable
            </div>

        </div>
        """
    )

    render_html(
        """
        <div class="workspace">

            <div class="workspace-label">
                Start an investigation
            </div>

            <div class="workspace-description">
                Describe the business outcome you want to understand.
                Nexus will turn the question into an investigation,
                analyze the available evidence, and produce a structured
                conclusion.
            </div>

        </div>
        """
    )

    question = st.text_area(
        "Investigation question",
        value=st.session_state.question_input,
        placeholder=(
            "Why did customer churn increase by 18% this quarter?"
        ),
        height=125,
        label_visibility="collapsed",
    )

    st.session_state.question_input = question

    col1, col2 = st.columns([1, 3])

    with col1:

        priority = st.selectbox(
            "Priority",
            [
                "low",
                "medium",
                "high",
                "critical",
            ],
            index=1,
        )

    with col2:

        st.write("")

        run_button = st.button(
            "◆  Run Investigation  →",
            type="primary",
            use_container_width=True,
        )

    # -----------------------------------------------------
    # EXAMPLES
    # -----------------------------------------------------

    render_html(
        """
        <div class="examples-label">
            Try an investigation
        </div>
        """
    )

    example_columns = st.columns(3)

    examples = [
        (
            "Churn",
            "Why did customer churn increase this quarter?",
        ),
        (
            "Customer Risk",
            "Which customer segment shows the strongest churn signal?",
        ),
        (
            "Product",
            "Is product change activity associated with customer churn?",
        ),
    ]

    for column, (category, example) in zip(
        example_columns,
        examples,
    ):

        with column:

            render_html(
                f"""
                <div class="example-card">

                    <div class="example-category">
                        {html.escape(category)}
                    </div>

                    <div class="example-question">
                        {html.escape(example)}
                    </div>

                </div>
                """
            )

            if st.button(
                "Use example",
                key=f"example_{category}",
                use_container_width=True,
            ):

                st.session_state.question_input = example

                st.rerun()


    # -----------------------------------------------------
    # PRODUCT PRINCIPLES
    # -----------------------------------------------------

    render_html(
        """
        <div class="principles">

            <div class="principle">
                <div class="principle-icon">◇</div>

                <div class="principle-title">
                    Validate the claim
                </div>

                <div class="principle-description">
                    Nexus checks what the evidence actually supports
                    instead of blindly accepting the question.
                </div>
            </div>

            <div class="principle">
                <div class="principle-icon">◈</div>

                <div class="principle-title">
                    Follow the evidence
                </div>

                <div class="principle-description">
                    Findings are ranked according to evidence strength,
                    consistency, and observed relationships.
                </div>
            </div>

            <div class="principle">
                <div class="principle-icon">◆</div>

                <div class="principle-title">
                    Respect causality
                </div>

                <div class="principle-description">
                    Associations are distinguished from established
                    causal relationships.
                </div>
            </div>

        </div>
        """
    )


    # -----------------------------------------------------
    # RUN
    # -----------------------------------------------------

    if run_button:

        if not question.strip():

            st.warning(
                "Enter an investigation question first."
            )

        else:

            try:

                with st.status(
                    "Nexus is investigating...",
                    expanded=True,
                ) as investigation_status:

                    st.write("◆ Planning investigation")

                    st.write("◇ Analyzing available evidence")

                    st.write("◇ Validating the stated claim")

                    st.write("◇ Evaluating potential root causes")

                    st.write("◇ Synthesizing investigation report")

                    investigation = create_investigation(
                        question=question.strip(),
                        priority=priority,
                    )

                    investigation_status.update(
                        label="Investigation complete",
                        state="complete",
                        expanded=False,
                    )

                st.session_state.investigation = investigation

                st.rerun()

            except requests.RequestException as exc:

                st.error(
                    f"Investigation request failed: {exc}"
                )

            except Exception as exc:

                st.error(
                    f"Unexpected error: {exc}"
                )

# =========================================================
# RESULT VIEW
# =========================================================

investigation = st.session_state.investigation

if investigation:

    investigation_id = investigation.get("id")

    # -----------------------------------------------------
    # Retrieve persisted result
    # -----------------------------------------------------

    if (
        investigation_id
        and not investigation.get("result")
    ):

        try:

            investigation = get_investigation(
                str(investigation_id)
            )

            st.session_state.investigation = investigation

        except requests.RequestException:

            pass


    result = (
        investigation.get("result")
        or {}
    )

    conclusion = (
        result.get("conclusion")
        or {}
    )

    root_analysis = (
        result.get("root_cause_analysis")
        or {}
    )

    # =====================================================
    # FINDINGS
    # =====================================================

    findings = (
        conclusion.get("findings")
        or []
    )

    if not findings:

        serialized_results = (
            result.get("results")
            or []
        )

        for item in serialized_results:

            if not isinstance(item, dict):
                continue

            if item.get("finding"):

                findings.append(
                    item["finding"]
                )

            elif item.get("findings"):

                nested_findings = item["findings"]

                if isinstance(
                    nested_findings,
                    list,
                ):

                    findings.extend(
                        nested_findings
                    )


    root_causes = (
        root_analysis.get("root_causes")
        or []
    )

    limitations = (
        root_analysis.get("limitations")
        or []
    )

    report = result.get("report")


    # =====================================================
    # RESULT HEADER
    # =====================================================

    render_html(
        """
        <div class="hero">

            <div class="hero-title">
                <span class="hero-mark">◆</span>
                INVESTIGATION <span class="hero-title-accent">COMPLETE</span>
            </div>

            <div class="hero-subtitle">
                Nexus has completed the investigation and assembled
                the available evidence into a structured analysis.
            </div>

        </div>
        """
    )


    # =====================================================
    # QUESTION CARD
    # =====================================================

    question_text = html.escape(
        str(
            investigation.get(
                "question",
                "",
            )
        )
    )

    render_html(
        f"""
        <div class="nexus-card">

            <div class="card-label">
                Investigation Question
            </div>

            <div
                style="
                    color:#F4F7FA;
                    font-size:1.12rem;
                    font-weight:620;
                    line-height:1.45;
                "
            >
                {question_text}
            </div>

        </div>
        """
    )


    # =====================================================
    # TIMELINE
    # =====================================================

    render_timeline()


    # =====================================================
    # METRICS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Status",
            str(
                investigation.get(
                    "status",
                    "unknown",
                )
            ).upper(),
        )

    with col2:

        st.metric(
            "Priority",
            str(
                investigation.get(
                    "priority",
                    "unknown",
                )
            ).upper(),
        )

    with col3:

        st.metric(
            "Confidence",
            format_confidence(
                investigation.get(
                    "confidence_score"
                )
            ),
        )

    with col4:

        st.metric(
            "Findings",
            len(findings),
        )


    st.divider()


    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    render_html(
        """
        <div class="section-label">
            EXECUTIVE SUMMARY
        </div>
        """
    )

    summary = (
        conclusion.get("summary")
        or conclusion.get("explanation")
        or ""
    )

    if summary:

        st.write(summary)

    else:

        st.info(
            "No executive summary available."
        )


    # =====================================================
    # CLAIM VALIDATION
    # =====================================================

    claim = conclusion.get(
        "claim_assessment"
    )

    if claim:

        render_html(
            """
            <div class="section-label">
                CLAIM VALIDATION
            </div>
            """
        )

        observed = claim.get(
            "observed_value"
        )

        if observed is None:

            observed_text = "N/A"

        else:

            try:

                observed_text = (
                    f"{float(observed):.2f}%"
                )

            except (
                TypeError,
                ValueError,
            ):

                observed_text = html.escape(
                    str(observed)
                )


        claim_text = html.escape(
            str(
                claim.get(
                    "claim",
                    "N/A",
                )
            )
        )

        claim_status = html.escape(
            str(
                claim.get(
                    "status",
                    "unknown",
                )
            ).upper()
        )

        explanation = html.escape(
            str(
                claim.get(
                    "explanation",
                    "",
                )
            )
        )


        render_html(
            f"""
            <div class="claim-card">

                <div class="claim-warning">
                    ⚠ {claim_status}
                </div>

                <div
                    style="
                        display:flex;
                        gap:6rem;
                        align-items:flex-end;
                    "
                >

                    <div>

                        <div class="claim-caption">
                            CLAIM
                        </div>

                        <div class="claim-number">
                            {claim_text}
                        </div>

                    </div>

                    <div>

                        <div class="claim-caption">
                            OBSERVED
                        </div>

                        <div class="claim-number">
                            {observed_text}
                        </div>

                    </div>

                </div>

                <div class="claim-explanation">
                    {explanation}
                </div>

            </div>
            """
        )


    # =====================================================
    # ROOT CAUSE
    # =====================================================

    render_html(
        """
        <div class="section-label">
            ROOT-CAUSE ANALYSIS
        </div>
        """
    )

    if root_causes:

        for index, cause in enumerate(
            root_causes,
            start=1,
        ):

            cause_title = html.escape(
                str(
                    cause.get(
                        "cause",
                        "Unknown",
                    )
                )
            )

            cause_explanation = html.escape(
                str(
                    cause.get(
                        "explanation",
                        "",
                    )
                )
            )

            confidence = cause.get(
                "confidence"
            )

            causal_status = html.escape(
                str(
                    cause.get(
                        "causal_status",
                        "unknown",
                    )
                )
            )

            render_html(
                f"""
                <div class="root-card">

                    <div class="root-index">
                        ROOT CAUSE CANDIDATE {index}
                    </div>

                    <div class="root-title">
                        {cause_title}
                    </div>

                    <div class="root-description">
                        {cause_explanation}
                    </div>

                    <div class="root-meta">
                        Confidence:
                        {format_confidence(confidence)}
                        &nbsp;&nbsp;•&nbsp;&nbsp;
                        Causal status:
                        {causal_status}
                    </div>

                </div>
                """
            )

    else:

        st.info(
            "No root-cause candidates identified."
        )


    # =====================================================
    # FINDINGS
    # =====================================================

    render_html(
        """
        <div class="section-label">
            EVIDENCE & FINDINGS
        </div>
        """
    )

    if findings:

        for index, finding in enumerate(
            findings,
            start=1,
        ):

            if not isinstance(
                finding,
                dict,
            ):

                finding = {
                    "title": str(finding),
                    "description": "",
                }


            finding_title = html.escape(
                str(
                    finding.get(
                        "title",
                        finding.get(
                            "cause",
                            finding.get(
                                "name",
                                "Finding",
                            ),
                        ),
                    )
                )
            )

            finding_description = html.escape(
                str(
                    finding.get(
                        "description",
                        finding.get(
                            "explanation",
                            "",
                        ),
                    )
                )
            )

            confidence = finding.get(
                "confidence"
            )


            render_html(
                f"""
                <div class="finding-card">

                    <div class="finding-number">
                        FINDING {index}
                    </div>

                    <div class="finding-title">
                        {finding_title}
                    </div>

                    <div class="finding-description">
                        {finding_description}
                    </div>

                </div>
                """
            )

            if confidence is not None:

                st.caption(
                    "Confidence: "
                    f"{format_confidence(confidence)}"
                )

    else:

        st.info(
            "No findings available."
        )


    # =====================================================
    # LIMITATIONS
    # =====================================================

    if limitations:

        render_html(
            """
            <div class="section-label">
                LIMITATIONS
            </div>
            """
        )

        for limitation in limitations:

            st.warning(
                str(limitation)
            )


    # =====================================================
    # FULL REPORT
    # =====================================================

    if report:

        render_html(
            """
            <div class="section-label">
                INVESTIGATION REPORT
            </div>
            """
        )

        with st.expander(
            "View full investigation report"
        ):

            st.text(
                str(report)
            )