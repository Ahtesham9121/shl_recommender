
class ConversationStateManager:

    def extract_latest_user_message(self, messages):

        user_messages = []

        for msg in messages:

            role = msg.get("role", "")
            content = msg.get("content", "")

            if role == "user":
                user_messages.append(content)

        if not user_messages:
            return ""

        return user_messages[-1]

    def build_context(self, messages):

        context = []

        for msg in messages:

            role = msg.get("role", "")
            content = msg.get("content", "")

            context.append(f"{role}: {content}")

        return "\n".join(context)
    def build_search_query(self, messages):

        user_parts = []

        for msg in messages:

            role = msg.get("role", "")
            content = msg.get("content", "")

            if role == "user":
                user_parts.append(content)

        return " ".join(user_parts)
