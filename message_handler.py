# message_handler.py

class MessageHandler:
    def __init__(self):
        # Initialize conversation with a default system prompt and initial AI message
        self.conversation = [
            (
                "system",
                "You are a a character and your character is described below."
            ),
            (
                "assistant",
                " "
            )
        ]

    def add_message(self, role, message):
        self.conversation.append((role, message))

    def get_conversation(self):
        return self.conversation

    def update_system_prompt(self, new_prompt):
        # Update the system prompt (first message in conversation)
        if self.conversation and self.conversation[0][0] == "system":
            self.conversation[0] = ("system", new_prompt)
        else:
            self.conversation.insert(0, ("system", new_prompt))

    def update_initial_ai_message(self, new_message):
        # Update the initial AI message (assistant's first message) if it exists; otherwise, insert it
        if len(self.conversation) > 1 and self.conversation[1][0] == "assistant":
            self.conversation[1] = ("assistant", new_message)
        else:
            self.conversation.insert(1, ("assistant", new_message))
