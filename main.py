import requests
from bs4 import BeautifulSoup
import pandas as pd


class Extract:
    def __init__(self, url):
        self.url = url

    def remove_suffix(self, text, suffix):
        if text.endswith(suffix):
            return text[:-len(suffix)]
        return text

    def scrappe(self):
        csv_file = []
        for page in range(0, 325):
            response = requests.get(self.url + str(page))
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                all_data = soup.find_all("div", {"class": "post views-row"})
                # print(all_data)

                for item in all_data:
                    dic = {}

                    title_element = item.find(
                        "h3",
                        {
                            "class": [
                                "Content Type : Reports title",
                                "Content Type : Topic title",
                                "Content Type : Blog title",
                                "Content Type : Evaluation title",
                                "Content Type : News title",
                                "Content Type : Reader publication title",
                                "Content Type : Basic page title",
                                "Content Type : Event title",
                                "Content Type : Multimedia title",
                                "Content Type : Expert title",
                                "Content Type : Podcast title"
                            ]
                        },
                    )
                    dic["Title"] = title_element.text if title_element else ""

                    source_element = item.find(
                        "span",
                        {
                            "class": [
                                "label-type label-type-web",
                                "label-type",
                                "label-type label-type-web",
                            ]
                        },
                    )
                    dic["Source"] = source_element.text if source_element else ""

                    content_element = item.find("span", {"class" : "nontrimmed" })
                    dic["Content"] = self.remove_suffix(content_element.text if content_element else "", " Show Less")


                    country_element = item.find(
                        "span", {"class": ["countrylist prepend-comma", "countrylist"]}
                    )
                    dic["Country"] = country_element.text if source_element else ""

                    content_type_element = item.find_all("em", {"class": "post-info"})[1]
                    dic["Content_Type"] = content_type_element.text if content_type_element else ""

                    date_element = item.find("em", {"class": "date"})
                    dic["Date"] = date_element.text if date_element else ""

                    csv_file.append(dic)

        df = pd.DataFrame(csv_file)
        df.fillna("", inplace=True)
        df.to_csv("scraped_data.csv", index=False)


if __name__ == "__main__":
    url = "https://ieg.worldbankgroup.org/ieg-search?search_api_fulltext=%22government%22&field_topic=All&content_type_1=&field_sub_category=All&field_organization_tags=All&type_2_op=not&type_2%5B0%5D=homepage_spotlight_feature&sort_by=search_api_relevance&sort_order=DESC&page="

    scraper = Extract(url)
    scraper.scrappe()
