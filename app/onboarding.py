import streamlit as st
from models.user_profile import UserProfile
from utils.db import save_profile


def show_onboarding() -> None:
    st.title("Welcome to your AI Health Coach")
    st.markdown(
        """
        I'm **Maya**, your personal wellness coach.

        Before we start, I'd love to learn a little about you so I can tailor
        every conversation to your unique goals and lifestyle.

        *This takes about 2 minutes.*
        """
    )

    _show_disclaimer()

    st.divider()
    st.subheader("Tell me about yourself")

    with st.form("onboarding_form", clear_on_submit=False):
        name = st.text_input(
            "What's your name?",
            placeholder="e.g. Sarah",
            help="I'll use this to personalize our conversations.",
        )

        goal = st.text_area(
            "What's your main wellness goal right now?",
            placeholder="e.g. I want to have more energy, sleep better, reduce stress, eat healthier...",
            height=80,
            help="Be as specific or as general as you like.",
        )

        dietary_preference = st.selectbox(
            "What best describes your dietary preference?",
            options=[
                "No preference / omnivore",
                "Vegetarian",
                "Vegan",
                "Pescatarian",
                "Gluten-free",
                "Dairy-free",
                "Mediterranean style",
                "Other / I'll describe in chat",
            ],
        )

        st.markdown("#### How are things going for you right now?")

        col1, col2, col3 = st.columns(3)

        with col1:
            sleep_quality = st.select_slider(
                "Sleep quality",
                options=["poor", "fair", "good"],
                value="fair",
                help="How well have you been sleeping overall?",
            )

        with col2:
            stress_level = st.select_slider(
                "Stress level",
                options=["low", "medium", "high"],
                value="medium",
                help="How stressed do you feel day-to-day?",
            )

        with col3:
            movement_level = st.select_slider(
                "Movement level",
                options=["sedentary", "light", "moderate", "active"],
                value="light",
                help="How physically active are you currently?",
            )

        health_concerns = st.text_area(
            "Any health concerns or context you'd like to share? (optional)",
            placeholder="e.g. I sit at a desk all day, I'm a shift worker, I've been feeling fatigued lately...",
            height=80,
            help="General context only — I'm not a medical professional and this is not a diagnosis.",
        )

        submitted = st.form_submit_button(
            "Start my wellness journey →",
            use_container_width=True,
            type="primary",
        )

    if submitted:
        errors = []
        if not name.strip():
            errors.append("Please enter your name.")
        if not goal.strip():
            errors.append("Please describe your wellness goal.")

        if errors:
            for e in errors:
                st.error(e)
            return

        profile = UserProfile(
            name=name.strip(),
            goal=goal.strip(),
            dietary_preference=dietary_preference,
            sleep_quality=sleep_quality,
            stress_level=stress_level,
            movement_level=movement_level,
            health_concerns=health_concerns.strip(),
        )

        save_profile(profile)
        st.session_state.user_profile = profile
        st.session_state.messages = []
        st.session_state.show_welcome = True
        st.rerun()


def _show_disclaimer() -> None:
    st.info(
        """
        **Medical Disclaimer**

        This app provides general wellness and lifestyle coaching only.
        It is **not** a substitute for professional medical advice, diagnosis, or treatment.
        Always consult a qualified healthcare provider for medical concerns, symptoms,
        medications, or any diagnosed health conditions.

        In an emergency, call your local emergency services immediately.
        """,
        icon="ℹ️",
    )
