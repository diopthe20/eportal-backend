import io
import os

import spacy
from pyresparser import ResumeParser, utils
from spacy.matcher import Matcher


class CustomerParser(ResumeParser):
    def __init__(self, text, skills_file=None, custom_regex=None):
        nlp = spacy.load("en_core_web_sm")
        custom_nlp = spacy.load("en_core_web_sm")
        self.__skills_file = skills_file
        self.__custom_regex = custom_regex
        self.__matcher = Matcher(nlp.vocab)
        self.__details = {
            "name": None,
            "email": None,
            "mobile_number": None,
            "skills": None,
            "college_name": None,
            "degree": None,
            "designation": None,
            "experience": None,
            "company_names": None,
            "no_of_pages": None,
            "total_experience": None,
        }

        self.__text = text
        self.__nlp = nlp(self.__text)
        self.__custom_nlp = custom_nlp(self.__text)
        self.__noun_chunks = list(self.__nlp.noun_chunks)
        self.__get_basic_details()



def parse(path: str):
    data = ResumeParser(path).get_extracted_data()
    return data
