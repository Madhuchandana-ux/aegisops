import streamlit as st

from app.agents.graph import (
    agent_graph,
    build_initial_state,
)
from app.security.auth import (
    authenticate_user,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AegisOps 2.0",
    page_icon="🛡️",
    layout="wide",
)


# ============================================================
# SESSION STATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================


def logout() -> None:
    """
    Clear the authenticated Streamlit session.
    """

    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.last_result = None

    st.rerun()


def run_agent(
    incident_id: str,
    description: str,
    caller: str,
    username: str,
    role: str,
):
    """
    Execute the same LangGraph workflow used by the backend.
    """

    state = build_initial_state(
        incident_text=description,
        incident_id=incident_id,
        caller=caller,
        username=username,
        user_role=role,
    )

    result = agent_graph.invoke(state)

    return result


def status_label(value: str) -> str:
    """
    Convert internal status values to display text.
    """

    if not value:
        return "UNKNOWN"

    return value.upper().replace("_", " ")


# ============================================================
# LOGIN PAGE
# ============================================================


if not st.session_state.authenticated:

    st.title("🛡️ AegisOps 2.0")

    st.subheader(
        "Autonomous IT Incident Resolution Agent"
    )

    st.write(
        "Secure agentic AI workflow for incident "
        "classification, knowledge retrieval, "
        "risk assessment, controlled automation, "
        "and verification."
    )

    st.divider()

    login_col1, login_col2, login_col3 = st.columns(
        [1, 2, 1]
    )

    with login_col2:

        st.header("Sign in")

        with st.form(
            "login_form",
            clear_on_submit=False,
        ):

            username = st.text_input(
                "Username",
                placeholder="Enter your AegisOps username",
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
            )

            login_button = st.form_submit_button(
                "Login",
                use_container_width=True,
            )

        if login_button:

            if not username.strip() or not password:

                st.error(
                    "Username and password are required."
                )

            else:

                try:

                    user = authenticate_user(
                        username=username.strip(),
                        password=password,
                    )

                    if user is None:

                        st.error(
                            "Invalid username or password."
                        )

                    else:

                        st.session_state.authenticated = True
                        st.session_state.username = (
                            user["username"]
                        )
                        st.session_state.role = user["role"]

                        st.success(
                            "Login successful."
                        )

                        st.rerun()

                except Exception as exc:

                    st.error(
                        f"Authentication failed: {exc}"
                    )

    st.divider()

    st.caption(
        "Development environment • SQLite • "
        "Local/mock ServiceNow • Mock LLM"
    )

    st.stop()


# ============================================================
# MAIN APPLICATION
# ============================================================


with st.sidebar:

    st.title("🛡️ AegisOps")

    st.caption(
        "Autonomous IT Incident Resolution"
    )

    st.divider()

    st.write("Logged in as")

    st.write(
        f"**{st.session_state.username}**"
    )

    st.write(
        f"Role: **{st.session_state.role}**"
    )

    st.divider()

    st.write("Execution mode")

    st.code(
        "LLM: MOCK\n"
        "ServiceNow: MOCK\n"
        "Database: SQLite",
        language="text",
    )

    st.divider()

    if st.button(
        "Logout",
        use_container_width=True,
    ):
        logout()


st.title(
    "🛡️ AegisOps 2.0 — Incident Resolution"
)

st.write(
    "Submit an IT incident and let the AegisOps "
    "agent classify, retrieve evidence, reason about "
    "the incident, evaluate risk, execute only "
    "authorized actions, and verify the result."
)

st.divider()


# ============================================================
# INCIDENT INPUT
# ============================================================


st.header("1. Submit Incident")

input_col1, input_col2 = st.columns(2)

with input_col1:

    incident_id = st.text_input(
        "Incident ID",
        value="INC0010001",
        help="Optional ServiceNow incident number.",
    )

with input_col2:

    caller = st.text_input(
        "Caller",
        value="employee01",
    )


description = st.text_area(
    "Incident Description",
    value=(
        "VPN connection fails when working from home."
    ),
    height=150,
    max_chars=5000,
)


st.caption(
    f"Characters: {len(description)} / 5000"
)


# ============================================================
# SAMPLE INCIDENTS
# ============================================================


st.subheader("Example incidents")

sample_col1, sample_col2, sample_col3 = (
    st.columns(3)
)

with sample_col1:

    if st.button(
        "VPN issue",
        use_container_width=True,
    ):

        description = (
            "VPN connection fails when working "
            "from home."
        )

        st.rerun()


with sample_col2:

    if st.button(
        "Outlook issue",
        use_container_width=True,
    ):

        description = (
            "Outlook is not opening and the "
            "application crashes repeatedly."
        )

        st.rerun()


with sample_col3:

    if st.button(
        "Printer issue",
        use_container_width=True,
    ):

        description = (
            "The office printer is not connecting "
            "to the employee laptop."
        )

        st.rerun()


st.divider()


# ============================================================
# EXECUTE AGENT
# ============================================================


run_button = st.button(
    "🚀 Analyze & Resolve Incident",
    type="primary",
    use_container_width=True,
)


if run_button:

    if len(description.strip()) < 5:

        st.error(
            "Incident description must contain "
            "at least 5 characters."
        )

    else:

        with st.spinner(
            "AegisOps agent is processing the incident..."
        ):

            try:

                result = run_agent(
                    incident_id=incident_id.strip(),
                    description=description.strip(),
                    caller=caller.strip(),
                    username=st.session_state.username,
                    role=st.session_state.role,
                )

                st.session_state.last_result = result

            except Exception as exc:

                st.session_state.last_result = None

                st.error(
                    f"Agent execution failed: {exc}"
                )


# ============================================================
# RESULTS
# ============================================================


result = st.session_state.last_result


if result is not None:

    st.divider()

    st.header("2. Agent Result")


    # ========================================================
    # TOP-LEVEL METRICS
    # ========================================================

    metric1, metric2, metric3, metric4 = (
        st.columns(4)
    )

    with metric1:

        st.metric(
            "Category",
            result.get(
                "category",
                "Unknown",
            ),
        )

    with metric2:

        confidence = result.get(
            "classification_confidence",
            0.0,
        )

        st.metric(
            "Confidence",
            f"{confidence:.1%}",
        )

    with metric3:

        st.metric(
            "Priority",
            result.get(
                "priority",
                "Unknown",
            ),
        )

    with metric4:

        st.metric(
            "Risk",
            result.get(
                "risk_level",
                "Unknown",
            ),
        )


    st.divider()


    # ========================================================
    # SECURITY / POLICY
    # ========================================================

    st.subheader("Security & Policy")

    security_col1, security_col2, security_col3 = (
        st.columns(3)
    )

    with security_col1:

        injection_detected = result.get(
            "prompt_injection_detected",
            False,
        )

        if injection_detected:

            st.error(
                "⚠️ Prompt injection detected"
            )

        else:

            st.success(
                "✅ No prompt injection detected"
            )

    with security_col2:

        policy_allowed = result.get(
            "policy_allowed",
            False,
        )

        if policy_allowed:

            st.success(
                "✅ Policy: ALLOWED"
            )

        else:

            st.warning(
                "⛔ Policy: BLOCKED"
            )

    with security_col3:

        requires_human = result.get(
            "requires_human",
            False,
        )

        if requires_human:

            st.warning(
                "👤 Human approval required"
            )

        else:

            st.success(
                "🤖 Automated path allowed"
            )


    policy_reason = result.get(
        "policy_reason",
        "",
    )

    if policy_reason:

        st.info(
            f"**Policy decision:** {policy_reason}"
        )


    st.divider()


    # ========================================================
    # RETRIEVAL
    # ========================================================

    st.subheader("Knowledge Retrieval")

    retrieved_documents = result.get(
        "retrieved_documents",
        [],
    )

    rag_col1, rag_col2 = st.columns(2)

    with rag_col1:

        st.metric(
            "Retrieved Documents",
            len(retrieved_documents),
        )

    with rag_col2:

        st.metric(
            "Retrieval Scores",
            len(
                result.get(
                    "retrieval_scores",
                    [],
                )
            ),
        )


    if retrieved_documents:

        with st.expander(
            "View retrieved knowledge-base documents",
            expanded=False,
        ):

            for index, document in enumerate(
                retrieved_documents,
                start=1,
            ):

                title = document.get(
                    "title",
                    f"Document {index}",
                )

                source = document.get(
                    "source",
                    "Unknown",
                )

                content = document.get(
                    "content",
                    "",
                )

                st.markdown(
                    f"**{index}. {title}**"
                )

                st.caption(
                    f"Source: {source}"
                )

                st.write(content)

                if index < len(
                    retrieved_documents
                ):

                    st.divider()


    # ========================================================
    # REASONING
    # ========================================================

    st.subheader("Agent Recommendation")

    proposed_resolution = result.get(
        "proposed_resolution",
        "",
    )

    if proposed_resolution:

        st.info(
            proposed_resolution
        )

    else:

        st.warning(
            "No resolution recommendation was generated."
        )


    st.divider()


    # ========================================================
    # SERVICE NOW ACTION
    # ========================================================

    st.subheader("Controlled ServiceNow Action")

    action_col1, action_col2, action_col3 = (
        st.columns(3)
    )

    with action_col1:

        st.write("**Target**")

        st.code(
            result.get(
                "servicenow_sys_id",
                "Not available",
            )
        )

    with action_col2:

        st.write("**Selected Action**")

        st.write(
            status_label(
                result.get(
                    "selected_action",
                    "unknown",
                )
            )
        )

    with action_col3:

        action_result = result.get(
            "action_result",
            {},
        )

        action_status = action_result.get(
            "status",
            "unknown",
        )

        st.write("**Execution Status**")

        if action_status == "executed":

            st.success("EXECUTED")

        elif action_status == "pending":

            st.warning("PENDING APPROVAL")

        elif action_status == "blocked":

            st.error("BLOCKED")

        else:

            st.warning(
                status_label(action_status)
            )


    action_result = result.get(
        "action_result",
        {},
    )

    action_message = action_result.get(
        "message",
        "",
    )

    if action_message:

        st.write(
            f"**Message:** {action_message}"
        )


    # ========================================================
    # VERIFICATION
    # ========================================================

    st.subheader("Act → Observe → Verify")

    verification = result.get(
        "verification_result",
        {},
    )

    verification_status = verification.get(
        "status",
        "unknown",
    )

    verified = verification.get(
        "verified",
        False,
    )


    verification_col1, verification_col2 = (
        st.columns(2)
    )

    with verification_col1:

        st.write("**Verification Status**")

        if verified:

            st.success(
                "✅ VERIFIED"
            )

        elif verification_status == "not_executed":

            st.warning(
                "NOT EXECUTED"
            )

        elif verification_status == "verification_failed":

            st.error(
                "❌ VERIFICATION FAILED"
            )

        else:

            st.warning(
                status_label(
                    verification_status
                )
            )


    with verification_col2:

        st.write("**Details**")

        st.write(
            verification.get(
                "message",
                "No verification message.",
            )
        )


    # ========================================================
    # HUMAN APPROVAL
    # ========================================================

    if requires_human:

        st.divider()

        st.header(
            "👤 Human-in-the-Loop"
        )

        st.warning(
            "This incident requires human approval "
            "before any external action can be performed."
        )

        st.write(
            "**Safety guarantee:** the current execution "
            "ended without executing a ServiceNow action."
        )

        st.info(
            "Approval-resume functionality will be added "
            "as the next workflow layer. The current agent "
            "correctly stops at the approval boundary."
        )


    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    st.divider()

    st.header("3. Final Response")

    final_response = result.get(
        "final_response",
        "",
    )

    if final_response:

        st.markdown(
            final_response
        )

    else:

        st.warning(
            "No final response was generated."
        )


    # ========================================================
    # TECHNICAL DETAILS
    # ========================================================

    with st.expander(
        "View technical execution details",
        expanded=False,
    ):

        st.write(
            "**Run ID:**",
            result.get(
                "run_id",
                "",
            ),
        )

        st.write(
            "**Username:**",
            result.get(
                "username",
                "",
            ),
        )

        st.write(
            "**Role:**",
            result.get(
                "user_role",
                "",
            ),
        )

        st.write(
            "**Classification Model:**",
            result.get(
                "classification_model",
                "",
            ),
        )

        st.write(
            "**Action Executed:**",
            result.get(
                "action_executed",
                False,
            ),
        )

        st.write(
            "**Step Count:**",
            result.get(
                "step_count",
                0,
            ),
        )

        errors = result.get(
            "errors",
            [],
        )

        if errors:

            st.error(
                "\n".join(errors)
            )

        else:

            st.success(
                "No agent errors reported."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AegisOps 2.0 • Agentic AI • LangGraph • "
    "Hybrid RAG • RBAC • Human-in-the-Loop • "
    "Controlled ServiceNow Automation"
)