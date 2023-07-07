from agent.pdf.models import PDFAgent

success_raw_data = PDFAgent.objects.filter(status=2)
data = []
for item in success_raw_data:
    data = data + item.raw_data.split("\n")
print(data)
