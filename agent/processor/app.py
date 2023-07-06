import pandas as pd

token_data = {
    "name": "DƯƠNG ĐÌNH",
    "email": "ddkhai@gmail.com",
    "mobile_number": "0794756838",
    "skills": [
        "Coaching",
        "R",
        "Teaching",
        "International",
        "Excel",
        "Content",
        "Sales",
        "English",
        "Mathematics",
        "Process",
        "Word",
        "P",
        "Safety",
        "Communication",
        "Repairs",
    ],
    "college_name": None,
    "degree": None,
    "designation": ["Mechanical Technician Assistant"],
    "experience": None,
    "company_names": ["MICROSOFT OFFICE SPECIALIST"],
    "no_of_pages": 2,
    "total_experience": 0,
}
text = open("agent/processor/text.txt", encoding="UTF-8").readlines()
data = " ".join(text)

token_data["raw_data"] = data
data = [
    token_data,
]
print(token_data)
df = pd.DataFrame.from_dict(data)
print(df)
