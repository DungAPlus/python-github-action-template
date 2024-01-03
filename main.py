import logging
import logging.handlers
import os

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")

   

    add_table_url = f'https://graph.microsoft.com/v1.0/sites/fbdd4069-e12d-4a30-b316-926cebd4972e/lists/fd860c96-4178-4c92-99b2-5f3fad37710e/items/10/driveitem/workbook/worksheets/Sheet1/tables/add'
    
    # Access Token
    token_url = f'https://login.microsoftonline.com/a3f88450-77ef-4df3-89ea-c69cbc9bc410/oauth2/v2.0/token'
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': 'ad6b066a-d749-4f0b-bfbb-bad8de0af5d1',
        'client_secret': 'TOc8Q~1zPMkTOOURFnPTFfC6ScwufbfrBSvuJaI8',
        'scope': 'https://graph.microsoft.com/.default'
    }
    
    token_r = requests.post(token_url, data=token_data)
    access_token = token_r.json()['access_token']
    
    # Headers
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
    }
    
    body = {
        "Address": "Sheet1!A1:G57",
        "hasHeaders": True
    }
    response = requests.post(add_table_url, headers=headers, json=body)
    
    if response.status_code == 201:
        logger.info(f'Tạo cấu trúc bảng thành công')
    else:
        logger.info(f'Có lỗi xảy ra khi tạo bảng. Lỗi: {response.content}')
    # r = requests.get('https://weather.talkpython.fm/api/weather/?city=Berlin&country=DE')
    # if r.status_code == 200:
    #     data = r.json()
    #     temperature = data["forecast"]["temp"]
    #     logger.info(f'Weather in Berlin: {temperature}')
