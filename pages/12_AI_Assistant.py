import streamlit as st

from chatbot.assistant import answer_question
from chatbot.data_engine import load_tables


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Life Insurance Renewal Intelligence",
    page_icon=None,
    layout="wide",
)


# ============================================================
# OVERVIEW-STYLE UI
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@10..48,600;10..48,700;10..48,800&family=DM+Sans:wght@400;500;600;700&display=swap');

    :root {
        --navy: #0e1b33;
        --blue: #2f6bd8;
        --blue-soft: #eaf1fd;
        --teal: #0f9b86;
        --teal-soft: #e3f6f2;
        --amber: #c97a0c;
        --amber-soft: #fdf0dc;
        --purple: #5b4bd6;
        --purple-soft: #eeecfd;
        --bg: #f3f6fb;
        --border: #e1e8f3;
        --muted: #71819a;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: var(--bg);
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        font-family: 'Bricolage Grotesque', sans-serif !important;
        color: var(--navy) !important;
    }

    .back-home {
        margin-bottom: 18px;
    }

    .back-home a {
        display: inline-flex !important;
        align-items: center !important;
        padding: 7px 15px !important;
        border-radius: 999px !important;
        border: 1px solid #d8e3f5 !important;
        background: #ffffff !important;
        color: var(--blue) !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        text-decoration: none !important;
        box-shadow: 0 2px 6px rgba(16,38,74,.05) !important;
    }

    .hero {
        background: linear-gradient(135deg, #0e1b33 0%, #172d55 100%);
        border-radius: 20px;
        padding: 34px 38px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(16,38,74,.10);
    }

    .hero-kicker {
        color: #9db8f5;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .10em;
        margin-bottom: 8px;
    }

    .hero-title {
        color: #ffffff;
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 38px;
        line-height: 1.1;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .hero-description {
        max-width: 820px;
        color: #dbe7ff;
        font-size: 15px;
        line-height: 1.65;
    }

    .hero-features {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 22px;
    }

    .hero-feature {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 7px 13px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,.12);
        background: rgba(255,255,255,.08);
        color: #edf3ff;
        font-size: 12px;
        font-weight: 600;
    }

    .hero-feature i {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }

    .section-heading {
        font-family: 'Bricolage Grotesque', sans-serif;
        color: var(--navy);
        font-size: 21px;
        font-weight: 800;
        margin: 26px 0 12px;
    }

    .info-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 14px rgba(16,38,74,.04);
        min-height: 100px;
    }

    .info-label {
        color: var(--muted);
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 6px;
    }

    .info-value {
        color: var(--navy);
        font-size: 23px;
        font-weight: 800;
    }

    .question-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 14px rgba(16,38,74,.04);
        margin-bottom: 14px;
    }

    .question-label {
        color: var(--blue);
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .06em;
        margin-bottom: 10px;
    }

    .question-text {
        color: var(--navy);
        font-size: 14px;
        font-weight: 600;
        line-height: 1.5;
    }

    .chat-note {
        background: var(--blue-soft);
        border: 1px solid #d6e4fb;
        border-radius: 14px;
        padding: 12px 16px;
        color: #31547f;
        font-size: 13px;
        line-height: 1.5;
        margin-bottom: 14px;
    }

    .nav-card {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 17px 19px;
        box-shadow: 0 4px 14px rgba(16,38,74,.04);
        min-height: 96px;
    }

    .nav-label {
        color: #7a8ca8;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .06em;
        margin-bottom: 5px;
    }

    .nav-title {
        color: var(--navy);
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 16px;
        font-weight: 800;
    }

    .nav-desc {
        color: #7a8ca8;
        font-size: 12px;
        margin-top: 4px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD PROJECT DATA
# ============================================================

if "ai_database" not in st.session_state:

    with st.spinner("Loading project data..."):

        (
            st.session_state.ai_database,
            st.session_state.ai_tables,
        ) = load_tables()


# ============================================================
# CHAT HISTORY
# ============================================================

if "ai_messages" not in st.session_state:

    st.session_state.ai_messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 I am your Life Insurance Analytics Assistant.\n\n"
                "You can ask me about insurers, premiums, renewals, "
                "forecasts, business insights or model performance."
            ),
        }
    ]


# ============================================================
# BACK TO HOME
# ============================================================

st.markdown('<div class="back-home">', unsafe_allow_html=True)
st.page_link("App.py", label="← Back to Home")
st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# HERO
# ============================================================

loaded_count = len(st.session_state.ai_tables)

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-kicker">AI-powered renewal intelligence</div>
        <div class="hero-title">Life Insurance AI Assistant</div>
        <div class="hero-description">
            Ask questions about life-insurance renewals, premiums, insurers,
            forecasts, business insights and model performance using natural language.
        </div>
        <div class="hero-features">
            <span class="hero-feature">
                <i style="background:#6ea8ff"></i>
                {loaded_count} datasets loaded
            </span>
            <span class="hero-feature">
                <i style="background:#5eead4"></i>
                Natural-language analytics
            </span>
            <span class="hero-feature">
                <i style="background:#fbbf5a"></i>
                SQL-backed answers
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ASSISTANT OVERVIEW
# ============================================================

st.markdown('<div class="section-heading">Assistant Workspace</div>', unsafe_allow_html=True)

info1, info2, info3 = st.columns(3)

with info1:
    st.markdown(
        '<div class="info-card"><div class="info-label">Data Sources</div>'
        f'<div class="info-value">{loaded_count}</div></div>',
        unsafe_allow_html=True,
    )

with info2:
    st.markdown(
        '<div class="info-card"><div class="info-label">Conversation Messages</div>'
        f'<div class="info-value">{len(st.session_state.ai_messages)}</div></div>',
        unsafe_allow_html=True,
    )

with info3:
    st.markdown(
        '<div class="info-card"><div class="info-label">Query Engine</div>'
        '<div class="info-value" style="font-size:18px">DuckDB + AI</div></div>',
        unsafe_allow_html=True,
    )


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================

st.markdown('<div class="section-heading">Example Questions</div>', unsafe_allow_html=True)

example_questions = [
    "Which insurer has the highest renewed premium?",
    "What is the overall renewal rate?",
    "Compare forecasting models using MAPE.",
    "Which model has the lowest average MAPE?",
    "Explain the forecast results.",
    "Show me the premium trend by insurer.",
]

question_cols = st.columns(2)

for index, question in enumerate(example_questions):
    with question_cols[index % 2]:
        st.markdown(
            f"""
            <div class="question-card">
                <div class="question-label">Suggested question</div>
                <div class="question-text">{question}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.markdown(
    '<div class="chat-note">💡 The assistant answers using the project CSV data and forecasting/model outputs. Type your question below to begin.</div>',
    unsafe_allow_html=True,
)


# ============================================================
# CHAT CONTROLS
# ============================================================

control_col1, control_col2 = st.columns([1, 5])

with control_col1:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.ai_messages = [
            {
                "role": "assistant",
                "content": "Chat cleared. What would you like to know?",
            }
        ]
        st.rerun()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

st.markdown('<div class="section-heading">Conversation</div>', unsafe_allow_html=True)

for message in st.session_state.ai_messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

user_question = st.chat_input(
    "Ask something about your life-insurance data..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if user_question:

    st.session_state.ai_messages.append(
        {
            "role": "user",
            "content": user_question,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):

        try:

            with st.spinner("Analyzing your data..."):

                (
                    answer,
                    sql_query,
                    result_df,
                ) = answer_question(
                    question=user_question,
                    connection=st.session_state.ai_database,
                    tables=st.session_state.ai_tables,
                    conversation_history=(
                        st.session_state.ai_messages[:-1]
                    ),
                )

            st.markdown(answer)

            with st.expander("🔎 Show data query used"):

                st.code(sql_query, language="sql")

                if result_df.empty:
                    st.info("The query returned no rows.")
                else:
                    st.dataframe(
                        result_df,
                        use_container_width=True,
                        hide_index=True,
                    )

            st.session_state.ai_messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except Exception as error:

            error_message = (
                "I couldn't answer that question.\n\n"
                "Please check your Gemini API key, the project data files, "
                "and the terminal error message."
            )

            st.error(error_message)

            with st.expander("Technical error"):
                st.code(str(error))

            st.session_state.ai_messages.append(
                {
                    "role": "assistant",
                    "content": error_message,
                }
            )


# ============================================================
# PAGE NAVIGATION
# ============================================================

st.markdown('<div class="section-heading">Continue Exploring</div>', unsafe_allow_html=True)

nav1, nav2 = st.columns(2)

with nav1:
    st.markdown(
        """
        <div class="nav-card">
            <div class="nav-label">Previous</div>
            <div class="nav-title">Duration Analysis</div>
            <div class="nav-desc">Analyze renewal performance across policy duration buckets.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link(
        "pages/11_Duration_Analysis.py",
        label="← Open Duration Analysis",
    )

with nav2:
    st.markdown(
        """
        <div class="nav-card">
            <div class="nav-label">Home</div>
            <div class="nav-title">Overview Dashboard</div>
            <div class="nav-desc">Return to the main life insurance intelligence dashboard.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.page_link(
        "pages/01_Overview.py",
        label="Open Overview →",
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#8a96a8;
        font-size:11px;
        margin-top:28px;
        padding-top:16px;
        border-top:1px solid #e6ebf2;
    ">
        Life Insurance Renewal Intelligence • AI Assistant
    </div>
    """,
    unsafe_allow_html=True,
)
