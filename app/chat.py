import streamlit as st
from core.coach import HealthCoach


_WELCOME_MESSAGE = """Hi {name}! I'm so glad you're here.

I've noted your goal: **{goal}** — that's a wonderful place to focus.

I'm Maya, your wellness coach. I'm here to support you with:
- 🥗 Nutrition and nourishing eating habits
- 😴 Sleep quality and rest
- 🧘 Stress management and mindset
- 🚶 Movement and gentle exercise
- 🌱 Building sustainable healthy habits

You can also use the quick actions in the sidebar to generate a **7-day wellness plan** or get **meal ideas** tailored to you.

To start — what's been feeling hardest for you lately when it comes to your wellness?
"""

_SPINNER_MESSAGES = {
    "wellness_plan": "Creating your personalized 7-day wellness plan...",
    "meal_ideas": "Putting together nourishing meal ideas for you...",
}


def show_chat(coach: HealthCoach) -> None:
    profile = st.session_state.user_profile

    # Display welcome message on first visit
    if st.session_state.get("show_welcome", False):
        welcome = _WELCOME_MESSAGE.format(
            name=profile.name,
            goal=profile.goal,
        )
        st.session_state.messages = [{"role": "assistant", "content": welcome}]
        st.session_state.show_welcome = False

    # Handle sidebar quick-action buttons
    pending = st.session_state.pop("pending_action", None)
    if pending == "wellness_plan":
        _handle_special_action(coach, profile, "wellness_plan")
    elif pending == "meal_ideas":
        _handle_special_action(coach, profile, "meal_ideas")

    # Render full chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=_avatar(msg["role"])):
            st.markdown(msg["content"])

    # Chat input
    if user_input := st.chat_input("Ask me anything about wellness, nutrition, sleep, or habits..."):
        # Append and render user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🙋"):
            st.markdown(user_input)

        # Stream assistant response
        with st.chat_message("assistant", avatar="🌿"):
            response_placeholder = st.empty()
            full_response = ""

            try:
                for token in coach.chat_stream(
                    user_message=user_input,
                    profile=profile,
                    history=st.session_state.messages[:-1],
                ):
                    full_response += token
                    response_placeholder.markdown(full_response + "▌")

                if full_response:
                    response_placeholder.markdown(full_response)
                else:
                    full_response = "_No response — model may be loading. Please wait a moment and try again._"
                    response_placeholder.warning(full_response)

            except Exception as e:
                full_response = f"_Error: {e}_"
                response_placeholder.error(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})


def _handle_special_action(coach: HealthCoach, profile, action: str) -> None:
    label = "Generating your 7-day wellness plan..." if action == "wellness_plan" else "Creating meal ideas for you..."
    user_prompt = "Please create my 7-day wellness plan." if action == "wellness_plan" else "Please give me some meal ideas."

    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.spinner(_SPINNER_MESSAGES[action]):
        if action == "wellness_plan":
            result = coach.generate_wellness_plan(profile)
        else:
            result = coach.generate_meal_ideas(profile)

    st.session_state.messages.append({"role": "assistant", "content": result})


def _avatar(role: str) -> str:
    return "🌿" if role == "assistant" else "🙋"
