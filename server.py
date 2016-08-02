# -*- coding: utf-8 -*-

import functools
import os
import pyautogui
import re
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
    with open('pikapika.gpx', mode='r', encoding='utf-8') as f:
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
    with open('pikapika.gpx', mode='w', encoding='utf-8') as f:
        f.write(template)


def change_location_(gps_button_pos, gpx_file_pos, lat_lng_string):

    def parse_latlng(lat_lng_string):
        return dict(re.findall(r'([latng]{3})\=([\d\.\-]+)', lat_lng_string))

    def click_button(pos):
        pyautogui.moveTo(pos)
        pyautogui.click()
    last_pos = pyautogui.position()
    lat_lng = parse_latlng(lat_lng_string)
    rewrite_gpx(lat_lng)
    click_button(gps_button_pos)
    click_button(gpx_file_pos)
    click_button(last_pos)


def get_button_position():
    print("GPS button에 커서를 올려주세요.")
    input("press enter to continue")
    gps_button_pos = pyautogui.position()
    print("GPX file에 커서를 올려주세요.")
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

        with open(os.getcwd() + '/map.html', 'rb') as fileHandle:
            self.wfile.write(fileHandle.read())

    def do_POST(self):
        self.set_headers()

        length = self.headers['content-length']
        data = self.rfile.read(int(length)).decode('utf-8')
        change_location(data)


if __name__ == '__main__':

    change_location = functools.partial(change_location_, *get_button_position())

    HTTPDeamon = HTTPServer(('', PORT), HTTPRequestHandler)
    _thread.start_new_thread(open_browser, ())
    try:
        HTTPDeamon.serve_forever()
    except KeyboardInterrupt:
        pass
    HTTPDeamon.server_close()
