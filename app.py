import html
import os
import re
import tempfile

import streamlit as st

from main import run_pipeline
from core.rag_engine import ask_question


st.set_page_config(
    page_title="Meeting Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        color-scheme: dark;

        --bg: #0B1120;
        --surface: #111827;
        --surface-2: #172033;
        --surface-3: #1E293B;

        --line: #293548;
        --line-hover: #3B4A61;

        --ink: #F8FAFC;
        --muted: #CBD5E1;
        --placeholder: #94A3B8;

        --accent: #14B8A6;
        --accent-dark: #0F766E;
        --accent-soft: #123B3A;

        --amber: #422006;
        --amber-ink: #FDE68A;

        --danger: #7F1D1D;
        --danger-ink: #FECACA;
    }


    /* =========================================================
       GLOBAL
       ========================================================= */

    html,
    body,
    button,
    input,
    textarea,
    [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: var(--bg) !important;
        color: var(--ink) !important;
    }

    .stApp {
        background: var(--bg) !important;
    }

    .block-container {
        padding-top: 1.6rem;
        max-width: 1120px;
    }

    #MainMenu,
    footer,
    header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0;
    }


    /* =========================================================
       GLOBAL TEXT
       ========================================================= */

    .stApp p,
    .stApp li,
    .stApp label,
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6,
    .stApp td,
    .stApp th,
    .stApp strong,
    .stApp em {
        color: var(--ink);
    }

    .stApp [data-testid="stCaptionContainer"],
    .stApp [data-testid="stCaptionContainer"] *,
    .stApp small {
        color: var(--muted) !important;
    }


    /* =========================================================
       SIDEBAR
       ========================================================= */

    section[data-testid="stSidebar"] {
        background: #0F172A !important;
        border-right: 1px solid var(--line) !important;
    }

    section[data-testid="stSidebar"] > div {
        background: #0F172A !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.2rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: .75rem;
        margin-bottom: 1.2rem;
    }

    .logo {
        width: 40px;
        height: 40px;
        border-radius: 11px;
        display: grid;
        place-items: center;
        font-size: 1.2rem;
        background: var(--accent);
        color: #FFFFFF !important;
    }

    .brand-name {
        font-weight: 800;
        font-size: 1.05rem;
        color: #FFFFFF !important;
        letter-spacing: -.01em;
    }

    .brand-sub {
        font-size: .78rem;
        color: var(--muted) !important;
    }

    .side-label {
        font-size: .8rem;
        font-weight: 700;
        color: var(--muted) !important;
        margin: 1.1rem 0 .35rem;
    }


    /* =========================================================
       RADIO
       ========================================================= */

    section[data-testid="stSidebar"] [data-testid="stRadio"] label,
    section[data-testid="stSidebar"] [data-testid="stRadio"] p,
    section[data-testid="stSidebar"] [data-testid="stRadio"] span {
        color: var(--ink) !important;
    }


    /* =========================================================
       INPUTS
       ========================================================= */

    .stApp [data-baseweb="input"],
    .stApp [data-baseweb="base-input"] {
        background: var(--surface-2) !important;
        border-radius: 10px;
    }

    .stApp [data-baseweb="input"] {
        border: 1px solid var(--line) !important;
    }

    .stApp input,
    .stApp textarea {
        color: var(--ink) !important;
        -webkit-text-fill-color: var(--ink) !important;
        background: transparent !important;
        caret-color: var(--accent) !important;
    }

    .stApp input::placeholder,
    .stApp textarea::placeholder {
        color: var(--placeholder) !important;
        -webkit-text-fill-color: var(--placeholder) !important;
        opacity: 1 !important;
    }

    .stApp [data-baseweb="input"]:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent) !important;
    }


    /* =========================================================
       FILE UPLOADER
       ========================================================= */

    [data-testid="stFileUploaderDropzone"] {
        background: var(--surface-2) !important;
        border: 1.5px dashed #475569 !important;
        border-radius: 12px;
    }

    [data-testid="stFileUploaderDropzone"] * {
        color: var(--ink) !important;
    }

    [data-testid="stFileUploaderDropzone"] small {
        color: var(--muted) !important;
    }

    [data-testid="stFileUploaderDropzone"] button {
        background: var(--surface-3) !important;
        color: var(--ink) !important;
        border: 1px solid var(--line-hover) !important;
    }

    [data-testid="stFileUploaderFile"] {
        background: var(--surface-2) !important;
    }

    [data-testid="stFileUploaderFile"] * {
        color: var(--ink) !important;
    }


    /* =========================================================
       TOGGLE
       ========================================================= */

    [data-testid="stToggle"] label,
    [data-testid="stToggle"] p,
    [data-testid="stToggle"] span {
        color: var(--ink) !important;
    }


    /* =========================================================
       BUTTONS
       ========================================================= */

    .stApp button {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .stApp button p,
    .stApp button span {
        color: inherit !important;
    }

    .stApp [data-testid="stBaseButton-secondary"],
    .stApp button[kind="secondary"],
    .stApp [data-testid="stDownloadButton"] button {
        background: var(--surface-2) !important;
        color: var(--ink) !important;
        border: 1px solid var(--line) !important;
        border-radius: 10px !important;
        font-weight: 600;
        width: 100%;
    }

    .stApp [data-testid="stBaseButton-secondary"]:hover,
    .stApp [data-testid="stDownloadButton"] button:hover {
        border-color: var(--accent) !important;
        color: var(--accent) !important;
    }

    .stApp [data-testid="stBaseButton-primary"],
    .stApp button[kind="primary"] {
        background: var(--accent) !important;
        color: #FFFFFF !important;
        border: 0 !important;
        border-radius: 10px !important;
        font-weight: 700;
        padding: .6rem 0;
        width: 100%;
    }

    .stApp [data-testid="stBaseButton-primary"] *,
    .stApp button[kind="primary"] * {
        color: #FFFFFF !important;
    }

    .stApp [data-testid="stBaseButton-primary"]:hover,
    .stApp button[kind="primary"]:hover {
        background: var(--accent-dark) !important;
    }


    /* =========================================================
       HERO
       ========================================================= */

    .hero {
        background: linear-gradient(135deg, #111827 0%, #123B3A 100%);
        border: 1px solid #263B4A;
        border-radius: 18px;
        padding: 2.5rem;
    }

    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -.03em;
        line-height: 1.15;
        margin-bottom: .7rem;
        color: #FFFFFF !important;
    }

    .hero-text {
        font-size: 1.02rem;
        line-height: 1.6;
        max-width: 640px;
        color: #CBD5E1 !important;
    }


    /* =========================================================
       FEATURES
       ========================================================= */

    .feature {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 1.2rem 1.3rem;
        height: 100%;
    }

    .feature .ic {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        background: var(--accent-soft);
        display: grid;
        place-items: center;
        font-size: 1.2rem;
        margin-bottom: .7rem;
    }

    .feature .h {
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: .3rem;
        color: var(--ink) !important;
    }

    .feature .t {
        font-size: .9rem;
        line-height: 1.55;
        color: var(--muted) !important;
    }


    /* =========================================================
       STEPS
       ========================================================= */

    .steps {
        display: flex;
        gap: 1rem;
        margin-top: 1.3rem;
        flex-wrap: wrap;
    }

    .step {
        flex: 1;
        min-width: 210px;
        display: flex;
        gap: .75rem;
        align-items: flex-start;
        font-size: .92rem;
        color: var(--ink) !important;
    }

    .step span {
        color: var(--muted) !important;
    }

    .step i {
        font-style: normal;
        flex: none;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: var(--accent);
        color: #FFFFFF !important;
        display: grid;
        place-items: center;
        font-weight: 700;
        font-size: .85rem;
    }


    /* =========================================================
       RESULTS
       ========================================================= */

    .title-card {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .badge {
        background: var(--accent-soft);
        color: #5EEAD4 !important;
        font-weight: 700;
        font-size: .78rem;
        padding: .3rem .75rem;
        border-radius: 999px;
    }

    .title-text {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -.02em;
        color: var(--ink) !important;
    }

    .stat {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 1rem 1.2rem;
    }

    .stat-num {
        font-size: 1.7rem;
        font-weight: 800;
        letter-spacing: -.02em;
        color: var(--ink) !important;
    }

    .stat-label {
        font-size: .83rem;
        color: var(--muted) !important;
    }


    /* =========================================================
       TABS
       ========================================================= */

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 1px solid var(--line);
        background: transparent !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--muted) !important;
        font-weight: 600;
        padding: .7rem 1rem;
        background: transparent !important;
    }

    .stTabs [data-baseweb="tab"] * {
        color: inherit !important;
    }

    .stTabs [aria-selected="true"] {
        color: #5EEAD4 !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        background: var(--accent) !important;
    }


    /* =========================================================
       CONTAINERS / CARDS
       ========================================================= */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--surface) !important;
        border: 1px solid var(--line) !important;
        border-radius: 14px;
    }

    [data-testid="stVerticalBlockBorderWrapper"] * {
        color: var(--ink);
    }


    /* =========================================================
       ITEMS
       ========================================================= */

    .item {
        display: flex;
        gap: .9rem;
        align-items: flex-start;
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: .95rem 1.1rem;
        margin-bottom: .6rem;
        color: var(--ink) !important;
        line-height: 1.55;
    }

    .item > div:last-child {
        color: var(--ink) !important;
    }

    .mark {
        flex: none;
        width: 24px;
        height: 24px;
        border-radius: 7px;
        display: grid;
        place-items: center;
        font-size: .8rem;
        font-weight: 800;
        margin-top: 1px;
    }

    .m-action {
        border: 2px solid var(--accent);
        color: var(--accent) !important;
    }

    .m-decision {
        background: var(--accent);
        color: #FFFFFF !important;
    }

    .m-question {
        background: var(--amber);
        color: var(--amber-ink) !important;
    }


    /* =========================================================
       EMPTY STATE
       ========================================================= */

    .empty {
        background: var(--surface);
        border: 1px dashed #475569;
        border-radius: 12px;
        padding: 1.6rem;
        text-align: center;
        color: var(--muted) !important;
    }


    /* =========================================================
       TRANSCRIPT
       ========================================================= */

    .transcript {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        max-height: 480px;
        overflow-y: auto;
        color: var(--ink) !important;
        line-height: 1.8;
        font-size: .95rem;
    }

    .transcript p {
        margin: 0 0 1rem;
        color: var(--ink) !important;
    }

    mark {
        background: #854D0E !important;
        color: #FEF3C7 !important;
        padding: 0 .15rem;
        border-radius: 3px;
    }


    /* =========================================================
       CHAT
       ========================================================= */

    [data-testid="stChatMessage"] {
        background: var(--surface) !important;
        border: 1px solid var(--line) !important;
        border-radius: 14px;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div {
        color: var(--ink) !important;
    }

    [data-testid="stChatInput"] {
        background: var(--surface) !important;
        border: 1px solid var(--line) !important;
        border-radius: 14px;
    }

    [data-testid="stChatInput"] textarea {
        color: var(--ink) !important;
        -webkit-text-fill-color: var(--ink) !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--placeholder) !important;
        -webkit-text-fill-color: var(--placeholder) !important;
    }


    /* =========================================================
       EXPANDER / STATUS
       ========================================================= */

    [data-testid="stExpander"],
    [data-testid="stStatusWidget"],
    details {
        background: var(--surface) !important;
        border: 1px solid var(--line) !important;
        border-radius: 12px;
    }

    [data-testid="stExpander"] *,
    [data-testid="stStatusWidget"] *,
    details * {
        color: var(--ink) !important;
    }


    /* =========================================================
       ALERTS
       ========================================================= */

    [data-testid="stAlert"] {
        background: var(--surface-2) !important;
        border: 1px solid var(--line) !important;
    }

    [data-testid="stAlert"] * {
        color: var(--ink) !important;
    }


    /* =========================================================
       SPINNER / STATUS
       ========================================================= */

    [data-testid="stSpinner"] {
        color: var(--muted) !important;
    }

    [data-testid="stSpinner"] * {
        color: var(--muted) !important;
    }


    /* =========================================================
       MARKDOWN LINKS
       ========================================================= */

    .stApp a {
        color: #5EEAD4 !important;
    }

    .stApp a:hover {
        color: #99F6E4 !important;
    }


    /* =========================================================
       SCROLLBAR
       ========================================================= */

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg);
    }

    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 999px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


def inline(text: str) -> str:
    escaped = html.escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)


def to_items(value) -> list[str]:
    if isinstance(value, (list, tuple)):
        return [str(v).strip() for v in value if str(v).strip()]

    items = []

    for line in str(value).splitlines():
        line = re.sub(r"^\s*(?:[-*•]|\d+[.)])\s+", "", line).strip()

        if line and not line.endswith(":"):
            items.append(line)

    return items


def render_items(items: list[str], kind: str, symbol: str, empty_msg: str):
    if not items:
        st.markdown(
            f'<div class="empty">{empty_msg}</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        "".join(
            f'<div class="item">'
            f'<div class="mark m-{kind}">{symbol}</div>'
            f'<div>{inline(i)}</div>'
            f'</div>'
            for i in items
        ),
        unsafe_allow_html=True,
    )


def as_bullets(value) -> str:
    return "\n".join(f"- {i}" for i in to_items(value))


st.session_state.setdefault("result", None)
st.session_state.setdefault("messages", [])
st.session_state.setdefault("pending", None)

result = st.session_state.result


with st.sidebar:

    st.markdown(
        '<div class="brand">'
        '<div class="logo">🎙️</div>'
        '<div>'
        '<div class="brand-name">Meeting Assistant</div>'
        '<div class="brand-sub">Transcribe, summarize, ask</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="side-label">Source</div>',
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "Source",
        ["YouTube link", "Upload file"],
        horizontal=True,
        label_visibility="collapsed",
    )

    url, upload = None, None

    if mode == "YouTube link":

        url = st.text_input(
            "YouTube URL",
            placeholder="https://youtube.com/watch?v=...",
            label_visibility="collapsed",
        )

    else:

        upload = st.file_uploader(
            "Audio or video file",
            type=[
                "mp3",
                "wav",
                "m4a",
                "mp4",
                "mkv",
                "webm",
                "mov",
            ],
            label_visibility="collapsed",
        )

    st.markdown(
        '<div class="side-label">Options</div>',
        unsafe_allow_html=True,
    )

    translate = st.toggle(
        "Translate audio to English",
        value=False,
    )

    st.write("")

    run = st.button(
        "Analyze meeting",
        type="primary",
    )

    if result:

        st.markdown(
            '<div class="side-label">Export</div>',
            unsafe_allow_html=True,
        )

        report = (
            f"# {result['title']}\n\n"
            f"## Summary\n{result['summary']}\n\n"
            f"## Action items\n{as_bullets(result['action_items'])}\n\n"
            f"## Key decisions\n{as_bullets(result['key_decisions'])}\n\n"
            f"## Open questions\n{as_bullets(result['questions'])}\n"
        )

        st.download_button(
            "Download report (.md)",
            report,
            "meeting_report.md",
            "text/markdown",
        )

        st.download_button(
            "Download transcript (.txt)",
            str(result["transcription"]),
            "transcript.txt",
        )

        st.write("")

        if st.button("Start over"):
            st.session_state.result = None
            st.session_state.messages = []
            st.session_state.pending = None
            st.rerun()


if run:

    source, tmp_path = None, None

    if url and url.strip():

        source = url.strip()

    elif upload is not None:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(upload.name)[1],
        ) as tmp:

            tmp.write(upload.getbuffer())
            source = tmp_path = tmp.name

    if not source:

        st.sidebar.error(
            "Paste a YouTube link or upload a file first."
        )

    else:

        st.session_state.messages = []

        try:

            with st.status(
                "Analyzing your meeting…",
                expanded=True,
            ) as status:

                st.write(
                    "Downloading audio, transcribing, and extracting "
                    "insights. This can take a few minutes."
                )

                st.session_state.result = run_pipeline(
                    source,
                    translate,
                )

                status.update(
                    label="Analysis complete",
                    state="complete",
                    expanded=False,
                )

            st.rerun()

        except Exception as e:

            st.session_state.result = None

            st.error(
                f"Something went wrong while processing: {e}"
            )

        finally:

            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)


if not result:

    st.markdown(
        '<div class="hero">'
        '<div class="hero-title">'
        'Turn any meeting into clear notes and answers.'
        '</div>'
        '<div class="hero-text">'
        'Add a YouTube link or a recording. You get a transcript, '
        'a summary, action items, key decisions, and a chat assistant '
        'that answers questions about what was said.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    features = [
        (
            "📝",
            "Summary and transcript",
            "A concise overview plus a full, searchable transcript.",
        ),
        (
            "✅",
            "Actions and decisions",
            "See what needs doing, what was decided, and what is still open.",
        ),
        (
            "💬",
            "Chat with the meeting",
            "Ask follow-up questions and get answers grounded in the recording.",
        ),
    ]

    for col, (icon, head, text) in zip(
        st.columns(3),
        features,
    ):

        col.markdown(
            f'<div class="feature">'
            f'<div class="ic">{icon}</div>'
            f'<div class="h">{head}</div>'
            f'<div class="t">{text}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="steps">'
        '<div class="step">'
        '<i>1</i>'
        '<span>Choose a YouTube link or upload a file in the sidebar.</span>'
        '</div>'
        '<div class="step">'
        '<i>2</i>'
        '<span>Select Analyze meeting and wait for processing to finish.</span>'
        '</div>'
        '<div class="step">'
        '<i>3</i>'
        '<span>Read the results, search the transcript, or ask questions.</span>'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.stop()


actions = to_items(result["action_items"])
decisions = to_items(result["key_decisions"])
questions = to_items(result["questions"])

transcript = str(result["transcription"])

words = len(transcript.split())


st.markdown(
    f'<div class="title-card">'
    f'<span class="badge">Analysis ready</span>'
    f'<span class="title-text">'
    f'{html.escape(str(result["title"]))}'
    f'</span>'
    f'</div>',
    unsafe_allow_html=True,
)


stats = [
    (f"{words:,}", "Words transcribed"),
    (f"~{max(1, words // 150)} min", "Estimated length"),
    (str(len(actions)), "Action items"),
    (str(len(decisions)), "Key decisions"),
]


for col, (num, label) in zip(
    st.columns(4),
    stats,
):

    col.markdown(
        f'<div class="stat">'
        f'<div class="stat-num">{num}</div>'
        f'<div class="stat-label">{label}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


st.write("")


t_sum, t_act, t_dec, t_q, t_tr, t_chat = st.tabs(
    [
        "Summary",
        f"Action items ({len(actions)})",
        f"Decisions ({len(decisions)})",
        f"Open questions ({len(questions)})",
        "Transcript",
        "Chat",
    ]
)


with t_sum:

    with st.container(border=True):
        st.markdown(result["summary"])


with t_act:

    render_items(
        actions,
        "action",
        "",
        "No action items were found in this meeting.",
    )


with t_dec:

    render_items(
        decisions,
        "decision",
        "✓",
        "No key decisions were found in this meeting.",
    )


with t_q:

    render_items(
        questions,
        "question",
        "?",
        "No open questions were found in this meeting.",
    )


with t_tr:

    query = st.text_input(
        "Search transcript",
        placeholder="Search for a word or phrase…",
        label_visibility="collapsed",
    )

    sentences = re.split(
        r"(?<=[.!?])\s+",
        transcript,
    )

    paras = [
        " ".join(sentences[i:i + 4])
        for i in range(0, len(sentences), 4)
    ]

    if query.strip():

        pattern = re.compile(
            re.escape(query.strip()),
            re.IGNORECASE,
        )

        paras = [
            p
            for p in paras
            if query.strip().lower() in p.lower()
        ]

        st.caption(
            f"{len(paras)} matching section(s)"
        )

        body = "".join(
            "<p>{}</p>".format(
                pattern.sub(
                    lambda m: f'<mark>{html.escape(m.group(0))}</mark>',
                    html.escape(p),
                )
            )
            for p in paras
        )

    else:

        body = "".join(
            f"<p>{html.escape(p)}</p>"
            for p in paras
        )

    st.markdown(
        f'<div class="transcript">'
        f'{body or "<p>No matches.</p>"}'
        f'</div>',
        unsafe_allow_html=True,
    )


with t_chat:

    if not st.session_state.messages:

        st.markdown("**Try asking:**")

        suggestions = [
            "What were the main topics?",
            "Who is responsible for what?",
            "Were any deadlines mentioned?",
            "Summarize this in three bullet points",
        ]

        for col, s in zip(
            st.columns(len(suggestions)),
            suggestions,
        ):

            if col.button(
                s,
                key=f"sug_{s}",
            ):

                st.session_state.pending = s
                st.rerun()

    for m in st.session_state.messages:

        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    prompt = (
        st.chat_input("Ask anything about this meeting…")
        or st.session_state.pending
    )

    st.session_state.pending = None

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Thinking…"):
                answer = ask_question(
                    result["rag_chain"],
                    prompt,
                )

            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )