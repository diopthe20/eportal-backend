import os
import pdfplumber
import spacy

nlp = spacy.load("xx_ent_wiki_sm")


def get_filtered_text(file_to_parse: str, size) -> str:
    with pdfplumber.open(file_to_parse) as pdf:
        text = pdf.pages[0]
        print(text)
        clean_text = text.filter(
            lambda obj: not (obj["object_type"] == "char" and obj["size"] < size)
        )
        return clean_text.extract_text()


def iterate(pdf, font_size_threshold, ner_filter):
    if font_size_threshold == 0:
        print("run out")
        return
    text = pdf.pages[0]
    filter_text = ""
    clean_text = text.filter(
        lambda obj: not (
            obj["object_type"] == "char" and obj["size"] < font_size_threshold
        )
    )

    doc = ner_filter(clean_text.extract_text())
    # for token in doc.ents:
    #     if token.label_:
    #         filter_text = token.text
    # condition = bool(filter_text == "")
    # if  condition:

    #     iterate(pdf, font_size_threshold-1, ner_filter)

    return doc


slider_value = 18
for filename in os.listdir("pdf-cv"):
    if filename.endswith("pdf"):
        print(filename)
        with pdfplumber.open(f"pdf-cv/{filename}") as pdf:
            value = iterate(pdf, 15, nlp)
            print(value)
            doc = nlp(value)

            for entity in doc.ents:
                print(f"{entity.label_} \t {entity}")
