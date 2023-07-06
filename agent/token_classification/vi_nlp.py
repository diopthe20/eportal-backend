import spacy

nlp = spacy.load("xx_ent_wiki_sm")
data = """
DƯƠNG ĐÌNH KHẢI

P R O D U CT I O N   E N G I N E E R   -   N E S T L E      
                                                                                                   
ABOUT ME
   
CONTACT

An  enthusiastic,  patient  and  dedicated  person  who
will  always  be  a  reliable  worker  for  the  production
department.  My  goal  is  to  become  an  outstanding
engineer  who  can  provide  the  highest-quality  work,
follow  to  safety
rules,  and  meet  all  project
requirements of production.

 29/09/2002

 ddkhai@gmail.com

 Tan Phu District, HCMC

 0794756838

EDUCATION

WORK EXPERIENCES

BACH KHOA UNIVERSITY
(HCMUT)

08/2020 - 08/2024

APOLLO ENGLISH

04/2022 - Present

Teaching Assistant - Private Tutor

School of Industrial Management

Studying in International Study Program (100%
using English)
National Highschool Graduation examination: 26,2
Ability test of National University of Ho Chi Minh
city: 939/1200.

"""
doc = nlp(data)
print(doc)
for entity in doc.ents:
    print(f"{entity.label_} \t {entity}")
