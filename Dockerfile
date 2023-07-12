FROM python:3.9.6

RUN mkdir /code
WORKDIR /code
COPY . /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python -c "import  nltk; nltk.download('stopwords')"
# Chạy backend
WORKDIR /code
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000","eportal.wsgi:application",]
