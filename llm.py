import os
from crewai import LLM


class GroqLLM(LLM):
    def call(self, messages, **kwargs):
        if isinstance(messages, list):
            cleaned_messages = []

            for message in messages:
                if isinstance(message, dict):
                    message = message.copy()
                    message.pop("cache_breakpoint", None)
                cleaned_messages.append(message)

            messages = cleaned_messages

        return super().call(messages, **kwargs)


def get_llm():
    return GroqLLM(
        model="groq/openai/gpt-oss-120b",
        api_key=os.environ["GROQ_API_KEY"],
        temperature=0.2,
    )
