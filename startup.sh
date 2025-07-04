# Assumes for now that you have a venv at .venv
# and also requirements are installed
# and mitmproxy is available in path
echo "Executing mitmproxy startup script"
source .venv/bin/activate
echo "Virtual environment activated"

echo "Generating request listener script"
python util/make.py Secure

echo "Running mitmproxy with blocker script"
mitmproxy -s mitm_script.py