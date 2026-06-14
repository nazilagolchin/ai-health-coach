import streamlit as st
from utils.db import clear_profile


def show_sidebar() -> None:
    with st.sidebar:
        st.image(
            "https://img.icons8.com/fluency/96/plant-under-sun.png",
            width=60,
        )
        st.title("AI Health Coach")
        st.caption("Your personal wellness companion")
        st.divider()

        profile = st.session_state.get("user_profile")

        if profile:
            _show_profile_card(profile)
            st.divider()
            _show_quick_actions()
            st.divider()

        _show_disclaimer()
        st.divider()
        _show_footer()


def _show_profile_card(profile) -> None:
    st.subheader(f"Hi, {profile.name}!")

    st.markdown("**Your goal**")
    st.caption(profile.goal)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sleep", profile.sleep_quality.capitalize())
        st.metric("Stress", profile.stress_level.capitalize())
    with col2:
        st.metric("Movement", profile.movement_level.capitalize())
        st.metric("Diet", _short_diet(profile.dietary_preference))

    if st.button("Reset profile", use_container_width=True):
        clear_profile()
        st.session_state.user_profile = None
        st.session_state.messages = []
        st.rerun()


def _show_quick_actions() -> None:
    st.markdown("**Quick actions**")

    if st.button("Create 7-day wellness plan", use_container_width=True):
        st.session_state.pending_action = "wellness_plan"
        st.rerun()

    if st.button("Get meal ideas", use_container_width=True):
        st.session_state.pending_action = "meal_ideas"
        st.rerun()

    if st.button("Clear chat history", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


def _show_disclaimer() -> None:
    st.markdown("**Disclaimer**")
    st.caption(
        "This app provides general wellness coaching only. "
        "It is not a substitute for professional medical advice. "
        "Always consult a doctor for medical concerns."
    )
    st.caption("🚨 **Emergency?** Call 911 or your local emergency number.")


def _show_footer() -> None:
    st.caption("Built with LangChain · ChromaDB · OpenAI · Streamlit")


def _short_diet(dietary_preference: str) -> str:
    mapping = {
        "No preference / omnivore": "Omnivore",
        "Other / I'll describe in chat": "Custom",
    }
    return mapping.get(dietary_preference, dietary_preference)
