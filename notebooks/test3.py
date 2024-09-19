from indexify_extractor_sdk import load_indexify_extractors, Content
from pydantic import BaseModel

# PDF extractor initialization
pdfextractor, pdfconfig_cls = load_indexify_extractors("indexify_extractors.pdfextractor.pdf_extractor:PDFExtractor")

# extract content from PDF file
content = Content.from_file("BalanceSheet.pdf")
config = pdfconfig_cls()

pdf_result = pdfextractor.extract(content, config)

# text content present in PDF
text_content = next(content.data.decode('utf-8') for content in pdf_result if content.content_type == 'text/plain')

# define schema
class Invoice(BaseModel):
    year: int
    captial_deposit: int
    total_liability: int
    total_assests: int
    ratio_of_assests_by_liabilities: float
    bills_collection: int
    increase_in_deposites_from_2021_to_2022: float

schema = Invoice.model_json_schema()

client = IndexifyClient()

extraction_graph_spec = f"""
name: 'pdf_schema_extractor'
extraction_policies:
  - extractor: 'tensorlake/marker'
    name: 'pdf_to_text'
  - extractor: 'tensorlake/schema'
    name: 'text_to_schema'
    input_params:
      service: 'openai'
      model_name: 'gpt-3.5-turbo'
      key: 'YOUR_OPENAI_API_KEY'
      schema_config: {schema}
      additional_messages: 'Extract information in JSON according to this schema and return only the output.'
    content_source: 'pdf_to_text'
"""

extraction_graph = ExtractionGraph.from_yaml(extraction_graph_spec)
result = client.create_extraction_graph(extraction_graph)
llm_content = next(content.data.decode("utf-8") for content in result if content.content_type == "text/plain")

# print all the attributes extracted
print(llm_content)