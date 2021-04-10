import pandas
import argparse

from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict

if __name__ == '__main__':    
    started_year = 1920
    total_years_number = datetime.today().year-started_year

    if total_years_number % 10 == 1 and total_years_number % 100 != 11:
        years = "год"
    elif 2 <= total_years_number % 10 <= 4 and not 12 <= total_years_number % 100 <= 14:
        years = "года"
    else:
        years = "лет"

    parser = argparse.ArgumentParser(
        description='Чтобы запустить сайт (index.html) вам потребуется указать название Exel файла с данными для вин'
    )
    parser.add_argument('file', default='wines.xlsx', nargs='?', help='Название файла')
    args = parser.parse_args().file

    wines = pandas.read_excel(args, sheet_name='Лист1', na_values='nan', keep_default_na=False).to_dict(orient='records')

    wine_assortment = defaultdict(list)
    for bottle in wines:
        wine_assortment[bottle['Категория']].append(bottle)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        total_years = total_years_number,
        years = years,
        wine_assortment = wine_assortment
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()