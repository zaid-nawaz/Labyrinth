from langchain_core.prompts import ChatPromptTemplate
from chains.parsers import parser

prompt = ChatPromptTemplate.from_template("""
You are answering questions about a YouTube video.

Rules:
- Answer only using the transcript context.
- Do not make up facts.
- If the answer cannot be answered using the transcript, explicitly state that the transcript does not contain the answer.
- Every factual claim should be supported by the transcript.
- Use the timestamp associated with the transcript segment that supports each claim.
- Only use timestamps that appear in the transcript context.
- DO NOT write timestamps, milliseconds, or timestamp markers such as [185200] in the answer content.
- The timestamps will be returned separately in the `offset` field.
- Keep the answer concise unless the user asks for more detail.

Transcript Context:
{context}

User Question:
{question}

{format_instruction}
""",
partial_variables={
    "format_instruction": parser.get_format_instructions()
})