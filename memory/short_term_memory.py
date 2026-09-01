from memory.memory_store import add_memory


class ShortTermMemory:
    """
    Stores the current conversation context.
    Also saves completed conversations to long-term memory.
    """

    def __init__(self):
        self.messages = []

    def add_message(self, role, content):

        self.messages.append({
            "role": role,
            "content": content
        })

    def get_messages(self):
        return self.messages

    def get_context(self):

        context = []

        for message in self.messages:

            context.append(
                f"{message['role']}: {message['content']}"
            )

        return "\n".join(context)

    def save_to_long_term_memory(self):

        if not self.messages:
            return

        conversation = self.get_context()

        add_memory(
            conversation,
            memory_type="conversation"
        )

    def clear(self):
        self.messages = []

