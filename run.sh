mkdir temp
apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
pip install camelot-py[all]
apt install ghostscript python3-tk