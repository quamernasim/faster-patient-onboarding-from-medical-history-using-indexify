# faster-patient-onboarding-from-medical-history-using-indexify


curl https://getindexify.ai | sh
./indexify server -d

apt-get install python3-venv
python3 -m venv venv
source venv/bin/activate
apt-get install poppler-utils
pip install indexify-extractor-sdk indexify paddleocr s3fs
indexify-extractor download tensorlake/paddleocr_extractor
indexify-extractor join-server


