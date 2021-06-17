import requests

def get_logos(domain):
  url = f"https://autocomplete.clearbit.com/v1/companies/suggest?query={domain}"
  headers = {
      'Accept': '*/*',
      'Host': 'autocomplete.clearbit.com',
      'Origin': 'https://clearbit.com',
      'Referer': 'https://clearbit.com/logo',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
      'Accept-Language': 'pt-PT,pt;q=0.8,en;q=0.5,en-US;q=0.3',
      'Connection':'keep-alive',
      'Accept-Encoding': 'gzip, deflate, br'
  }
  try:
    response = requests.get(url, headers=headers)
    return response.json()[0]['logo']
  except:
    return ''



# domain='bbc.co.uk'
# out = get_logos(domain)
# print(out)