# faster-patient-onboarding-from-medical-history-using-indexify


curl https://getindexify.ai | sh
./indexify server -d

curl -fsSL https://ollama.com/install.sh | sh

apt-get install python3-venv
python3 -m venv venv
source venv2/bin/activate
apt-get install poppler-utils
pip install indexify-extractor-sdk indexify 
pip install paddleocr s3fs
indexify-extractor download tensorlake/paddleocr_extractor
indexify-extractor download tensorlake/schema
indexify-extractor join-server







https://docs.getindexify.ai/usecases/rag
https://github.com/tensorlakeai/indexify/tree/main/examples/pdf/indexing_and_rag
https://github.com/tensorlakeai/indexify-extractors/blob/main/text/schema/schema_extractor.py
https://github.com/tensorlakeai/indexify/tree/main/examples/pdf/langchain
https://docs.getindexify.ai/docs/getting-started-basic
https://pub.towardsai.net/structured-financial-data-extraction-from-unstructured-data-ca2c8d166de6
https://ai.gopubby.com/data-framework-for-llms-indexify-rag-application-project-b77295bab8ab