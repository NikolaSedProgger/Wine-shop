import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import pandas
from collections import defaultdict

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

current_date = f'{datetime.date.today()}'
year_started = 1920

wines = pandas.read_excel('wine3.xlsx', sheet_name='Лист1', na_values='nan', keep_default_na=False).to_dict(orient='records')
wine_assortment = defaultdict(list)
for bottle in wines:
    wine_assortment[bottle['Категория']].append(bottle)
    

rendered_page = template.render(
    years=int(current_date[:4])-year_started,
    wine_assortment=wine_assortment
)


with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()