def format_docs(retrieved_docs):
  context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
  return context_text

def format_timestamp(retrieved_docs):
  context_timestamp = [doc.metadata["start_offset"] for doc in retrieved_docs]
  return context_timestamp