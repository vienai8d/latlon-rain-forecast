import requests
import json
from datetime import datetime
from argparse import ArgumentParser

URL = 'https://map.yahooapis.jp/weather/V1/place'

def post_to_slack(url, message):
    if url:
        requests.post(url, headers={'content-type': 'application/json'}, data=json.dumps({'text': message}))

def get_weather(lat, lon, app_id):
    payload = dict(
        coordinates=f'{lat},{lon}',
        appid=app_id,
        output='json'
    )
    return requests.get(URL, params=payload)


def main():
    parser = ArgumentParser()
    parser.add_argument('app_id')
    parser.add_argument('latitude')
    parser.add_argument('longitude')
    parser.add_argument('-s', '--slack')
    parser.add_argument('--debug', action='store_true', default=False)
    args = parser.parse_args()

    # get weather infomation from yahooapi.
    payload = dict(
        coordinates=f'{args.latitude},{args.longitude}',
        appid=args.app_id,
        output='json'
    )
    r = requests.get(URL, params=payload)

    if args.debug:
        print(f'[DEBUG] {r.json()}')

    weather = r.json()['Feature'][0]['Property']['WeatherList']['Weather']
    msg_list = []
    for w in weather:
        t = w['Type']
        p = w['Rainfall']
        dt = datetime.strptime(w['Date'], '%Y%m%d%H%M')

        if args.debug:
            print(f'[DEBUG] {t}, {dt}, {p}')

        if t == 'observation':
            continue

        if args.debug or p > 0:
            msg_list.append(f'{dt}: p={p}')

    if msg_list:
        post_to_slack(args.slack, '\n'.join(msg_list))

if __name__ == '__main__':
    main()