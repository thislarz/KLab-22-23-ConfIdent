

from random import seed
import requests
from urllib.request import Request, urlopen

url = "https://www.gamefaqs.com"
results = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
print(results)
"""
session_obj = requests.Session()
response = session_obj.get(url, headers={"User-Agent": "Mozilla/5.0"})

print(response.status_code)

request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
webpage = urlopen(request_site).read()
print(webpage[:500])

print(response)
"""