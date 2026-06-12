import streamlit as st
from agent.tools.send_email import send_email
from agent.loop import SalesOpsAgent
from agent.memory import trim_conversation
from agent.logging_utils import log_tool_call

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = SalesOpsAgent()

if "pending_email" not in st.session_state:
    st.session_state.pending_email = None

agent = st.session_state.agent

st.set_page_config(
    page_title="Sales Ops Assistant",
    layout="wide"
)

st.title("Sales Ops Assistant")

with st.sidebar:

    st.header("Session Stats")

    st.metric(
        "Session Cost (₹)",
        round(
            agent.safety.session_cost,
            4
        )
    )

    st.metric(
        "Cost Remaining (₹)",
        round(
            20 - agent.safety.session_cost,
            4
        )
    )

    st.metric(
        "Messages",
        len(st.session_state.messages)
    )

    if agent.safety.session_cost > 15:
        st.warning(
            "Approaching session cost limit."
        )

    if agent.safety.session_cost >= 20:
        st.error(
            "Cost limit reached."
        )

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Disable chat when cost limit reached
if agent.safety.session_cost >= 20:
    user_input = None

    st.info(
        "Chat disabled because session cost limit has been reached."
    )
else:
    user_input = st.chat_input(
        "Ask the Sales Ops Assistant..."
    )

if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Build full conversation history
    conversation = [
        {
            "role": msg["role"],
            "content": msg["content"]
        }
        for msg in st.session_state.messages
    ]
    conversation=trim_conversation(conversation)
    with st.chat_message("assistant"):

        with st.spinner("Working..."):
            try:
                result = agent.run(
                    conversation
                )
            except Exception as e:
                st.error(f"Agent Error: {e}")
                st.stop()

        st.markdown(
            result["response"]
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["response"]
        }
    )

    tool_history = result.get(
        "tool_history",
        []
    )

    for call in tool_history:

        with st.expander(
            f"Tool: {call['tool']}"
        ):

            st.json(
                {
                    "input": call["input"],
                    "output": call["output"]
                }
            )
        if call["tool"]=="draft_email":
            tool_output=call["output"]

            if tool_output["success"] and "result" in tool_output:
                draft=tool_output["result"]

                if draft.get("status")=="approval_required":
                    st.session_state.pending_email=draft

    st.caption(
        f"""
Iterations: {result.get('iterations', 0)}

Cost: ₹{result.get('cost', 0):.4f}
"""
    )

if st.session_state.pending_email:

    email = (
        st.session_state.pending_email
    )

    st.divider()

    st.subheader(
        "Email Approval Required"
    )

    st.write(
        f"To: {email['recipient']}"
    )

    st.write(
        f"Subject: {email['subject']}"
    )

    edited_body = st.text_area(
        "Email Body",
        value=email["body"],
        height=250
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Discard Draft"
        ):

            st.session_state.pending_email = None

            st.rerun()

    with col2:

        if st.button(
            "Send Email"
        ):
            result = send_email(
                recipient=email["recipient"],
                subject=email["subject"],
                body=edited_body if edited_body != None else ""
            )

            try:
                log_tool_call(
                    "send_email",
                    {
                        "recipient":
                            email["recipient"],
                        "subject":
                            email["subject"]
                    },
                    result,
                    0
                )
            except Exception:
                pass

            st.success(
                result["message"]
            )

            st.session_state.pending_email = None

            st.rerun()

if st.button("Clear Session"):

    st.session_state.messages = []

    st.session_state.agent = SalesOpsAgent()

    st.rerun()