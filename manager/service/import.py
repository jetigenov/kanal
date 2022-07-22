from __future__ import print_function
from datetime import datetime
import requests
import xmltodict
from googleapiclient.discovery import build
from google.oauth2 import service_account

from db_home.models import db, Order


def update_sheet(bag):
    """
    Function for update from database to my google sheet
    REQUEST_METHOD = POST
    BODY = { }
    """
    SERVICE_ACCOUNT_FILE = '../kanal.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    # The ID of my spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1WqF3fiyrt3sWPd_fRGVdDKk98P4q_6Y23TJu8xWBkfI'

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    orders = db.session.query(Order).all()
    for o in orders:
        data = [[o.id, o.order_id, o.amount, str(o.shipping_date), o.amount]]

        request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range='Sheet1!A2:D2', valueInputOption='USER_ENTERED',
                                        insertDataOption='INSERT_ROWS',
                                        body={'values': data}).execute()


def save_data(d):
    """
    Function for save data to Postgres database
    """
    order = db.session.query(Order).filter(Order.order_id == d['заказ №']).first()
    if not order:
        o = Order()
        date = datetime.strptime(d['срок поставки'], '%d/%m/%Y')
        o.order_id = d['заказ №']
        o.cost = d['стоимость в $']
        o.shipping_date = date
        o.amount = d['стоимость в RUB']

        db.session.add(o)
        db.session.commit()


def get_currency(i):
    """
    Function for get currency from currency API
    """
    new_list = []

    date = datetime.strptime(i[3], '%d.%m.%Y')
    reformat_date = date.strftime('%d/%m/%Y')  # formatting date because url not accepting 'divider'

    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    params = {"date_req": reformat_date}
    currencies = requests.get(url, params=params)
    parser = xmltodict.parse(currencies.text)  # parsing xml to dict

    items = parser['ValCurs']['Valute'] if parser['ValCurs'] else []

    for k in items:
        if k.get('NumCode') == '840':  # choosing USD by international currency iso code
            new_list.append({
                '№': int(i[0]),
                'заказ №': i[1],
                'стоимость в $': i[2],
                'срок поставки': reformat_date,
                'стоимость в RUB': float(i[2]) * float(k.get('Value').replace(",", "."))
            })

    for d in new_list:
        save_data(d)


def get_sheet(bag):
    """
    Function for get a sheet from google account by sheet id
    REQUEST_METHOD = POST
    BODY = { }
    """
    SERVICE_ACCOUNT_FILE = '../kanal.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    # ID of a spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1f-qZEX1k_3nj5cahOzntYAnvO4ignbyesVO7yuBdv_g'

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range='Лист1!A2:D51').execute()

    for i in result['values']:
        get_currency(i)
