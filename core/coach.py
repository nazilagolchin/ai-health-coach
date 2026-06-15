import os
from typing import Generator
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from core.prompts import (
    HEALTH_COACH_SYSTEM_PROMPT,
    WELLNESS_PLAN_PROMPT,
    MEAL_IDEAS_PROMPT,
)
from core.rag import HealthKnowledgeBase
from core.safety import check_safety
from models.user_profile import UserProfile


class HealthCoach:
    """Orchestrates safety check → RAG retrieval → LLM call."""

    def __init__(self, knowledge_base: HealthKnowledgeBase):
        self.kb = knowledge_base
        self.llm = ChatAnthropic(
            model=os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5"),
            temperature=0.7,
            streaming=True,
        )

    def _build_system_message(self, profile: UserProfile, rag_context: str) -> SystemMessage:
        content = HEALTH_COACH_SYSTEM_PROMPT.format(
            user_profile=profile.to_coach_context(),
            rag_context=rag_context if rag_context else "No additional context retrieved.",
        )
        return SystemMessage(content=content)

    def _history_to_langchain(self, history: list[dict]) -> list:
        messages = []
        for msg in history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        return messages

    def chat_stream(
        self,
        user_message: str,
        profile: UserProfile,
        history: list[dict],
    ) -> Generator[str, None, None]:
        """Yield response tokens one at a time for streaming display."""

        is_unsafe, safety_response = check_safety(user_message)
        if is_unsafe:
            yield safety_response
            return

        rag_context = self.kb.retrieve(user_message)

        system_msg = self._build_system_message(profile, rag_context)
        history_msgs = self._history_to_langchain(history)
        current_msg = HumanMessage(content=user_message)

        all_messages = [system_msg] + history_msgs + [current_msg]

        for chunk in self.llm.stream(all_messages):
            if chunk.content:
                yield chunk.content

    def generate_wellness_plan(self, profile: UserProfile) -> str:
        """Generate a 7-day wellness plan (non-streaming, returns full text)."""
        prompt = WELLNESS_PLAN_PROMPT.format(
            name=profile.name,
            user_profile=profile.to_coach_context(),
            goal=profile.goal,
            dietary_preference=profile.dietary_preference,
        )
        llm_non_stream = ChatAnthropic(
            model=os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5"),
            temperature=0.7,
        )
        response = llm_non_stream.invoke([HumanMessage(content=prompt)])
        return response.content

    def generate_meal_ideas(self, profile: UserProfile) -> str:
        """Generate 5 nourishing meal ideas (non-streaming, returns full text)."""
        prompt = MEAL_IDEAS_PROMPT.format(
            name=profile.name,
            dietary_preference=profile.dietary_preference,
            goal=profile.goal,
        )
        llm_non_stream = ChatAnthropic(
            model=os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5"),
            temperature=0.7,
        )
        response = llm_non_stream.invoke([HumanMessage(content=prompt)])
        return response.content
