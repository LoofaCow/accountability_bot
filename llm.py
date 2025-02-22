# llm.py

import os
from langchain_openai import ChatOpenAI

class LLM:
    def __init__(self):
        # Initialize the LLM with your featherless API key and settings
        self.llm = ChatOpenAI(
            api_key="rc_e6ec09ba80c982892db6e937ac4cabb71f6c0b8a14c44c1b9081eb682d67a0f5",
            base_url="https://api.featherless.ai/v1",
            model="mistralai/Mistral-Nemo-Instruct-2407",
        )

    def get_response(self, conversation):
        # Get the LLM response based on the conversation history
        return self.llm.invoke(conversation)
