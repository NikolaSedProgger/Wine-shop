from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import pandas
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader, select_autoescape
import argparse

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

year_started = 1920
years = datetime.today().year-year_started
last_year_num = int(list(str(years))[-1])

if last_year_num == 1:
    a = "год"
elif last_year_num >= 2 and last_year_num < 5:
    a = "года"
elif last_year_num >= 5 and last_year_num < 10 or last_year_num == 0:
    a = "лет"

parser = argparse.ArgumentParser(
    description='Чтобы запустить сайт (index.html) вам потребуется указать название Exel файла с данными для вин'
)
parser.add_argument('file', help='Название файла')
args = parser.parse_args().file

try:
    wines = pandas.read_excel(args, sheet_name='Лист1', na_values='nan', keep_default_na=False).to_dict(orient='records')
except:
    print("Файла, который вы указали, не существует. Использован wines.xlsx")
    wines = pandas.read_excel("wines.xlsx", sheet_name='Лист1', na_values='nan', keep_default_na=False).to_dict(orient='records')


wine_assortment = defaultdict(list)
for bottle in wines:
    wine_assortment[bottle['Категория']].append(bottle)

rendered_page = template.render(
    a = a,
    years=years,
    wine_assortment=wine_assortment
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()