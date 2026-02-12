from pdf_function.riyasat_pdf import generate_acknowledgement_pdf as riyasat_pdf
from pdf_function.happy_pdf import generate_acknowledgement_pdf as happy_pdf
from pdf_function.bhumija_pdf import generate_acknowledgement_pdf as bhumija_pdf


class client:
    def __init__(self, name, id, s3_bucket, pdf_function):
        self.name = name
        self.id = id
        self.s3_bucket = s3_bucket
        self.pdf_function = pdf_function


clients = {
    "riyasat": client(name="Riyasat Builders", id=1, s3_bucket="scheme-application-files", pdf_function=riyasat_pdf),
    "happy": client(name="Happy Builders", id=2, s3_bucket="happy-scheme-application-files", pdf_function=happy_pdf),
    "bhumija": client(name="Bhumija Builders", id=3, s3_bucket="bhumija-scheme-application-files", pdf_function=bhumija_pdf)
}
     