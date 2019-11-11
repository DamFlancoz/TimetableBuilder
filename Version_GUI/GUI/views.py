from time import localtime
from datetime import date, timedelta

from django.shortcuts import render

# Create your views here.

# Subjects list
subjs = [
    "AGEI",
    "ANTH",
    "ART",
    "AE",
    "AHVS",
    "ASTR",
    "BIOC",
    "BCMB",
    "BIOL",
    "BME",
    "BUS",
    "CS",
    "CHEM",
    "CYC",
    "CIVE",
    "HUFA",
    "COM",
    "CD",
    "CSC",
    "EDCI",
    "DR",
    "EOS",
    "ECON",
    "ED-D",
    "EDUC",
    "ECE",
    "ENGR",
    "ENGL",
    "ENT",
    "ER",
    "ES",
    "EUS",
    "EPHE",
    "FA",
    "FORB",
    "FRAN",
    "GNDR",
    "GEOG",
    "GMST",
    "GS",
    "GRS",
    "HINF",
    "HLTH",
    "HS",
    "HSTR",
    "HDCC",
    "ICDG",
    "IED",
    "IGOV",
    "IN",
    "INGH",
    "IS",
    "IET",
    "INTD",
    "IB",
    "INTS",
    "KINE",
    "LAS",
    "LAW",
    "LING",
    "MRNE",
    "MGB",
    "MBA",
    "MATH",
    "MECH",
    "MEDS",
    "MEDI",
    "MICR",
    "MUS",
    "NRSC",
    "NURS",
    "NUNP",
    "NUHI",
    "PAAS",
    "PHIL",
    "PHYS",
    "POLI",
    "PSYC",
    "ADMN",
    "PADR",
    "PHSP",
    "RHED",
    "RS",
    "SMGT",
    "SLST",
    "SDH",
    "SJS",
    "SOCW",
    "SOCI",
    "SENG",
    "SPAN",
    "STAT",
    "TS",
    "THEA",
    "VIRS",
    "WKEX",
    "WRIT",
]


# Create your views here.
def main(request):

    # termOptions = getTermOptions()
    termOptions = ["201901", "201905", "201909"]

    context = {
        "termOptions": make_code_terms(),
        "subjs": subjs,
        "days": ["M", "T", "W", "R", "F"],
    }

    return render(request, "GUI/main.html", context)


# Helper
def make_code_terms():

    months_4 = timedelta(days=4 * 30.5)
    current = date.today()

    for i in range(3):
        year, month, *_ = (current + months_4 * i).timetuple()
        yield get_code(year, month), get_term(year, month)


def get_term(year, month):
    if month in [1, 2, 3, 4]:
        term = f"Spring {year}"

    elif month in [5, 6, 7, 8]:
        term = f"Summer {year}"

    else:
        term = f"Fall {year}"

    return term


def get_code(year, month):
    if month in [1, 2, 3, 4]:
        code = f"{year}01"

    elif month in [5, 6, 7, 8]:
        code = f"{year}05"

    else:
        code = f"{year}09"

    return code
