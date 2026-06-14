from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UserProfile:
    name: str
    goal: str
    dietary_preference: str
    sleep_quality: str       # "poor" | "fair" | "good"
    stress_level: str        # "low" | "medium" | "high"
    movement_level: str      # "sedentary" | "light" | "moderate" | "active"
    health_concerns: str = ""

    def to_coach_context(self) -> str:
        """Returns a plain-text summary for injection into the system prompt."""
        lines = [
            f"Name: {self.name}",
            f"Main wellness goal: {self.goal}",
            f"Dietary preference: {self.dietary_preference}",
            f"Current sleep quality: {self.sleep_quality}",
            f"Current stress level: {self.stress_level}",
            f"Current movement/activity level: {self.movement_level}",
        ]
        if self.health_concerns.strip():
            lines.append(f"Health concerns (self-reported): {self.health_concerns}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "goal": self.goal,
            "dietary_preference": self.dietary_preference,
            "sleep_quality": self.sleep_quality,
            "stress_level": self.stress_level,
            "movement_level": self.movement_level,
            "health_concerns": self.health_concerns,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "UserProfile":
        return cls(
            name=data["name"],
            goal=data["goal"],
            dietary_preference=data["dietary_preference"],
            sleep_quality=data["sleep_quality"],
            stress_level=data["stress_level"],
            movement_level=data["movement_level"],
            health_concerns=data.get("health_concerns", ""),
        )
