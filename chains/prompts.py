from langchain_core.prompts import ChatPromptTemplate
from chains.parsers import parser

prompt = ChatPromptTemplate.from_template("""
You are answering questions about a YouTube video.

Rules:
- Answer only using the transcript context.
- Do not make up facts.
- If the answer cannot be answered using the transcript, explicitly state that the transcript does not contain the answer. Do not use outside knowledge.
- Cite the timestamp(s) from the context whenever possible.
- Keep the answer concise unless the user asks for more detail.

Transcript Context:
{context}
                                          
Timestamp:
{timestamp}

User Question:
{question}

{format_instruction}
""",
partial_variables={'format_instruction' : parser.get_format_instructions()}
)