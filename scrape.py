import requests
from bs4 import BeautifulSoup



url = "https://ieg.worldbankgroup.org/ieg-search?search_api_fulltext=%22government%22&field_topic=All&content_type_1=&field_sub_category=All&field_organization_tags=All&type_2_op=not&type_2%5B0%5D=homepage_spotlight_feature&sort_by=search_api_relevance&sort_order=DESC&page=0"


response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

data = soup.find("div", class_ = "post views-row")

print(data.text)