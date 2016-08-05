# -*- coding: utf-8 -*-

import os
import pyautogui
import re
import sys
import time
import webbrowser
import _thread

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode

PORT = 8080
GPX_FILENAME = 'pikapika.gpx'


def open_browser():
    # http://stackoverflow.com/questions/22445217/python-webbrowser-open-to-open-chrome-browser
    try:
        params = get_last_location()
    except OSError:
        params = ''
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    url = 'http://localhost:{}/?{}'.format(PORT, params)
    print(url)
    time.sleep(1)
    webbrowser.get(chrome_path).open(url)


def get_last_location():
    with open(GPX_FILENAME, mode='r', encoding='utf-8') as f:
        xml = f.read()
    l = re.findall(r'([laton]{3})="([\d.-]+)"', xml)
    return urlencode(dict(l))


def rewrite_gpx(lat_lng):
    template = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
                  <gpx xmlns="http://www.topografix.com/GPX/1/1" version="1.1"
                      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                      xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
                      <wpt lat="{lat}" lon="{lng}"></wpt>
                  </gpx>'''.format(**lat_lng)
    with open(GPX_FILENAME, mode='w', encoding='utf-8') as f:
        f.write(template)


def change_location_(js_develop_mode, gps_button_pos, gpx_file_pos):
    def real_change(lat_lng_string):
        if js_develop_mode:
            return
        last_pos = pyautogui.position()
        lat_lng = dict(re.findall(r'([latng]{3})\=([\d\.\-]+)', lat_lng_string))
        rewrite_gpx(lat_lng)
        for pos in gps_button_pos, gpx_file_pos, last_pos:
            pyautogui.click(*pos)

    return real_change


def initialize():
    if not os.getenv('GOOGLE_API_KEY'):
        print('*' * 80)
        print('You must set GOOGLE_API_KEY to OS environments.')
        print('Please check https://developers.google.com/maps/documentation/javascript/get-api-key')
        print("export GOOGLE_API_KEY='blahblah' to ~/.bash_profile")
        print('*' * 80)
        raise NameError('GOOGLE_API_KEY')

    print("Cursor on GPS button of xcode.")
    input("press enter to continue")
    gps_button_pos = pyautogui.position()
    print("Cursor on GPX file of xcode. (pikapika.gpx)")
    input("press enter to continue")
    gpx_file_pos = pyautogui.position()
    return gps_button_pos, gpx_file_pos


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        self.set_headers()

        api_key = bytes(os.getenv('GOOGLE_API_KEY').encode('utf-8'))
        with open(os.getcwd() + '/map.html', 'rb') as fileHandle:
            html = fileHandle.read()
            html = html.replace(b'{{GOOGLE_MAP_API_KEY}}', api_key)
            self.wfile.write(html)

    def do_POST(self):
        self.set_headers()

        length = self.headers['content-length']
        data = self.rfile.read(int(length)).decode('utf-8')
        change_location(data)


if __name__ == '__main__':
    js_dev_mode = sys.argv[-1] == 'jsdev'
    change_location = change_location_(js_dev_mode, *initialize())

    HTTPDeamon = HTTPServer(('', PORT), HTTPRequestHandler)
    _thread.start_new_thread(open_browser, ())
    try:
        HTTPDeamon.serve_forever()
    except KeyboardInterrupt:
        pass
    HTTPDeamon.server_close()
