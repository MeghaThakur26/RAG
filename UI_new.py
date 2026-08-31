
print("STEP 1: Starting application")

import streamlit as st

print("STEP 2: Streamlit imported")

from langchain_core.messages import HumanMessage, ToolMessage

import time

print("STEP 3: LangChain messages imported")

start_time = time.time()

from Agents import llm_tools, tools

print(
    f"STEP 4: Agents imported successfully "
    f"({time.time() - start_time:.2f} seconds)"
)

# ============================================================
# PAGE CONFIG
# ============================================================

print("STEP 5: Setting page configuration")

st.set_page_config(
    page_title="City Intelligence",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

print("STEP 6: Page configuration completed")


# ============================================================
# CUSTOM CSS
# ============================================================

print("STEP 7: Loading CSS")

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .stApp {
        background-color: #f7f8fc;
        color: #111827;
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }


    /* ========================================================
       REMOVE DEFAULT STREAMLIT ELEMENTS
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent;
    }


    /* ========================================================
       HEADER
       ======================================================== */

    .main-title {
        font-size: 40px;
        font-weight: 750;
        text-align: center;
        color: #111827 !important;
        margin-top: 10px;
        margin-bottom: 4px;
        letter-spacing: -0.8px;
    }

    .subtitle {
        text-align: center;
        color: #6b7280 !important;
        font-size: 16px;
        margin-bottom: 35px;
        line-height: 1.5;
    }


    /* ========================================================
       CHAT MESSAGE AREA
       ======================================================== */

    [data-testid="stChatMessage"] {
        padding: 14px 18px;
        margin-bottom: 12px;
        border-radius: 14px;
    }

    /* Make ALL chat text black */
    [data-testid="stChatMessage"],
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div {
        color: #111827 !important;
    }

    /* User message */
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background-color: #e8eefc;
        border: 1px solid #dbe3f5;
    }

    /* Assistant message */
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }


    /* ========================================================
       MARKDOWN / TEXT
       ======================================================== */

    .stMarkdown,
    .stMarkdown p,
    .stMarkdown li,
    .stMarkdown span {
        color: #111827 !important;
    }

    p {
        line-height: 1.65;
    }


    /* ========================================================
       TOOL APPROVAL CARD
       ======================================================== */

    .approval-box {
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #dbe3f5;
        background-color: #ffffff;
        margin-top: 20px;
        margin-bottom: 18px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
    }

    .approval-title {
        font-size: 18px;
        font-weight: 650;
        color: #111827 !important;
        margin-bottom: 8px;
    }

    .approval-description {
        font-size: 14px;
        color: #6b7280 !important;
        line-height: 1.5;
    }

    .tool-name {
        font-weight: 700;
        color: #111827 !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 10px 16px;
        font-size: 15px;
        font-weight: 600;
        border: 1px solid #d1d5db;
        background-color: #ffffff;
        color: #111827 !important;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #9ca3af;
        background-color: #f9fafb;
    }


    /* ========================================================
       CHAT INPUT
       ======================================================== */

    [data-testid="stChatInput"] {
        border-radius: 14px;
    }

    [data-testid="stChatInput"] textarea {
        color: #111827 !important;
        background-color: #ffffff !important;
        font-size: 15px;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #9ca3af !important;
    }


    /* ========================================================
       DIVIDER
       ======================================================== */

    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin-top: 28px;
        margin-bottom: 28px;
    }


    /* ========================================================
       GENERAL STREAMLIT TEXT
       ======================================================== */

    .stApp label,
    .stApp small,
    .stApp span {
        color: #111827;
    }

    </style>
    """,
    unsafe_allow_html=True
)

print("STEP 8: CSS loaded successfully")


# ============================================================
# SESSION STATE
# ============================================================

print("STEP 9: Initializing session state")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_tool_calls" not in st.session_state:
    st.session_state.pending_tool_calls = []

if "final_answer" not in st.session_state:
    st.session_state.final_answer = None

print("STEP 10: Session state initialized")


# ============================================================
# HEADER
# ============================================================

print("STEP 11: Creating UI header")

st.markdown(
    '<div class="main-title">🌍 City Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Ask about the weather or latest news for a city'
    '</div>',
    unsafe_allow_html=True
)

print("STEP 12: UI header created")


# ============================================================
# DISPLAY PREVIOUS CONVERSATION
# ============================================================

print("STEP 13: Displaying previous conversation")

for message in st.session_state.messages:

    # --------------------------------------------------------
    # USER MESSAGE
    # --------------------------------------------------------

    if isinstance(message, HumanMessage):

        with st.chat_message("user"):

            st.markdown(
                message.content
            )


    # --------------------------------------------------------
    # ASSISTANT MESSAGE
    # --------------------------------------------------------

    elif hasattr(message, "content") and message.content:

        # Tool messages should not appear as normal messages
        if not isinstance(message, ToolMessage):

            with st.chat_message("assistant"):

                st.markdown(
                    message.content
                )

print("STEP 14: Previous conversation displayed")


# ============================================================
# TOOL APPROVAL
# ============================================================

print("STEP 15: Checking pending tool calls")

if st.session_state.pending_tool_calls:

    print("STEP 16: Pending tool call found")

    tool_call = st.session_state.pending_tool_calls[0]

    tool_name = tool_call["name"]


    # --------------------------------------------------------
    # APPROVAL CARD
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="approval-box">

            <div class="approval-title">
                🔧 Tool Approval Required
            </div>

            <div class="approval-description">
                The agent wants to use:
                <span class="tool-name">{tool_name}</span>
            </div>

            <div class="approval-description"
                 style="margin-top: 6px;">
                Please approve this action to continue.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # APPROVE / DENY BUTTONS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "✓  Approve",
            use_container_width=True
        ):

            print(
                f"STEP 17: Approving tool: {tool_name}"
            )

            tool_result = tools[tool_name].invoke(
                tool_call
            )

            print(
                "STEP 18: Tool executed successfully"
            )

            st.session_state.messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                )
            )

            st.session_state.pending_tool_calls = []

            st.rerun()


    with col2:

        if st.button(
            "✕  Deny",
            use_container_width=True
        ):

            print(
                f"STEP 19: Denying tool: {tool_name}"
            )

            st.session_state.messages.append(
                ToolMessage(
                    content=(
                        "Tool call denied. "
                        "I cannot get the latest information."
                    ),
                    tool_call_id=tool_call["id"]
                )
            )

            st.session_state.pending_tool_calls = []

            st.rerun()


# ============================================================
# CONTINUE AGENT AFTER TOOL EXECUTION
# ============================================================

print(
    "STEP 20: Checking whether agent needs to continue"
)

if (
    not st.session_state.pending_tool_calls
    and st.session_state.messages
):

    last_message = st.session_state.messages[-1]


    # --------------------------------------------------------
    # TOOL MESSAGE → CONTINUE AGENT
    # --------------------------------------------------------

    if isinstance(last_message, ToolMessage):

        print(
            "STEP 21: Last message is ToolMessage"
        )

        print(
            "STEP 22: Invoking LLM"
        )

        result = llm_tools.invoke(
            st.session_state.messages
        )

        print(
            "STEP 23: LLM invocation completed"
        )

        st.session_state.messages.append(
            result
        )


        # ----------------------------------------------------
        # ANOTHER TOOL REQUIRED
        # ----------------------------------------------------

        if result.tool_calls:

            print(
                "STEP 24: LLM requested another tool"
            )

            st.session_state.pending_tool_calls = (
                result.tool_calls
            )


        # ----------------------------------------------------
        # FINAL ANSWER
        # ----------------------------------------------------

        else:

            print(
                "STEP 25: LLM returned final answer"
            )

            st.session_state.final_answer = (
                result.content
            )

        st.rerun()


# ============================================================
# USER INPUT
# ============================================================

print(
    "STEP 26: Creating chat input"
)

user_input = st.chat_input(
    "Ask about a city's weather or latest news..."
)

print(
    "STEP 27: Chat input created"
)


# ============================================================
# PROCESS USER INPUT
# ============================================================

if user_input:

    print(
        "STEP 28: User entered input"
    )


    # --------------------------------------------------------
    # ADD USER MESSAGE
    # --------------------------------------------------------

    human_message = HumanMessage(
        content=user_input
    )

    st.session_state.messages.append(
        human_message
    )


    # --------------------------------------------------------
    # INVOKE AGENT
    # --------------------------------------------------------

    print(
        "STEP 29: Invoking LLM with user message"
    )

    result = llm_tools.invoke(
        st.session_state.messages
    )

    print(
        "STEP 30: LLM invocation completed"
    )


    # --------------------------------------------------------
    # SAVE AGENT RESPONSE
    # --------------------------------------------------------

    st.session_state.messages.append(
        result
    )


    # --------------------------------------------------------
    # AGENT REQUESTS TOOL
    # --------------------------------------------------------

    if result.tool_calls:

        print(
            "STEP 31: Agent requested a tool"
        )

        st.session_state.pending_tool_calls = (
            result.tool_calls
        )


    # --------------------------------------------------------
    # AGENT ANSWERS DIRECTLY
    # --------------------------------------------------------

    else:

        print(
            "STEP 32: Agent returned direct answer"
        )

        st.session_state.final_answer = (
            result.content
        )


    st.rerun()


# ============================================================
# APPLICATION COMPLETE
# ============================================================

print(
    "STEP 33: Application finished loading"
)

