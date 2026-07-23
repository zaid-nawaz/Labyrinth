


from langchain_core.prompts import ChatPromptTemplate
from chains.parsers import parser

prompt = ChatPromptTemplate.from_template("""
You are answering questions about a YouTube video.

Rules:
- Answer only using the transcript context.
- Do not make up facts.
- If the answer is not in the transcript, say you couldn't find it.
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