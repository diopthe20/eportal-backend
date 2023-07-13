mkdir temp
mk pdf-cv
apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
pip install camelot-py[cv]
apt install -Y ghostscript python3-tk
pip install ghostscript