FROM python:3.9.6

RUN mkdir /code
WORKDIR /code
COPY . /code
ADD requirements.txt /code/
RUN apt update
RUN apt update && apt-get install ffmpeg libsm6 libxext6 -y
RUN mkdir -p temp
RUN mkdir -p output
RUN mkdir -p pdf-cv
RUN apt install ghostscript python3-tk -y
RUN pip install ghostscript
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python -c "import  nltk; nltk.download('stopwords')"
# Chạy backend
WORKDIR /code
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000","eportal.wsgi:application",]
