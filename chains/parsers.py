from langchain_core.output_parsers import PydanticOutputParser
from schema.response import output

parser = PydanticOutputParser(pydantic_object=output)