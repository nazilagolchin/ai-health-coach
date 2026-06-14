import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Page config must be first Streamlit call
st.set_page_config(
    page_title="AI Health Coach | Maya",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "AI Health Coach built with LangChain, ChromaDB, and OpenAI. General wellness coaching only — not a medical service.",
    },
)

from utils.db import load_profile
from core.rag import HealthKnowledgeBase
from core.coach import HealthCoach
from app.onboarding import show_onboarding
from app.chat import show_chat
from app.sidebar import show_sidebar


@st.cache_resource(show_spinner="Loading health knowledge base...")
def _load_knowledge_base() -> HealthKnowledgeBase:
    kb = HealthKnowledgeBase(
        docs_dir=os.getenv("KNOWLEDGE_DIR", "data/knowledge"),
        persist_dir=os.getenv("CHROMA_PERSIST_DIR", "data/chroma_db"),
    )
    kb.load()
    return kb


def _validate_api_key() -> bool:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key or api_key.startswith("sk-your-"):
        st.error(
            "**OpenAI API key not configured.**\n\n"
            "1. Copy `.env.example` to `.env`\n"
            "2. Add your OpenAI API key\n"
            "3. Restart the app\n\n"
            "Get your key at [platform.openai.com](https://platform.openai.com/api-keys)",
            icon="🔑",
        )
        return False
    return True


def main() -> None:
    # Initialize session state defaults
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = load_profile()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Always render sidebar
    show_sidebar()

    if not _validate_api_key():
        return

    # Route: onboarding or chat
    if st.session_state.user_profile is None:
        show_onboarding()
    else:
        kb = _load_knowledge_base()
        coach = HealthCoach(knowledge_base=kb)
        show_chat(coach)


if __name__ == "__main__":
    main()
