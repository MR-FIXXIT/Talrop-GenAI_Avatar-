def format_for_avatar(
    system_prompt: str,
    memory: list[str],
    rag_context: str | None,
    web_context: str | None,
    user_message: str
) -> str:
    """
    Builds a short, spoken-style prompt for avatars
    """

    prompt = system_prompt + "\n\n"

    if memory:
        prompt += "Conversation so far:\n"
        for line in memory[-6:]:
            prompt += f"{line}\n"
        prompt += "\n"

    if rag_context:
        prompt += "Knowledge:\n"
        prompt += rag_context + "\n\n"

    if web_context:
        prompt += "Fresh information:\n"
        prompt += web_context + "\n\n"

    prompt += (
        "Respond naturally in short spoken sentences. "
        "Optionally include one emotion tag like [emotion: happy].\n\n"
    )

    prompt += f"User: {user_message}\nAssistant:"

    return prompt
