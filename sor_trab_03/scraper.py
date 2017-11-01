import urllib.request
import re
import requests
import json

def get_url_data(output, url):
    r = requests.get(url)
    url_open = r.text

    article = "<article id=\"post-"
    article_pos = 0
    rel_bookmark = "rel=\"bookmark\">"
    rel_bookmark_pos = 0

    while True:
        article_pos = url_open.find(article, rel_bookmark_pos)

        if article_pos == -1:
            break

        rel_bookmark_pos = url_open.find(rel_bookmark, article_pos)
        key = url_open[rel_bookmark_pos + len(rel_bookmark): url_open.find("</",
                                                                           rel_bookmark_pos)]

        paragraph_data = url_open[
                         url_open.find("<p>", rel_bookmark_pos) + 3: url_open.find(
                             "<a class=\"moretag\"", rel_bookmark_pos)]

        paragraph_words = paragraph_data.split()

        result = ""
        did_break = False
        for word in paragraph_words:
            if word.isalnum() and word != key:
                result += " " + word
            else:
                break

        if (len(result) > 0 and result != key):
            output[key] = result




if __name__ == "__main__":

    result = {}

    urls = ["https://www.siglaseabreviaturas.com/informatica/",
            "https://www.siglaseabreviaturas.com/informatica/page/2/",
            "https://www.siglaseabreviaturas.com/informatica/page/3/",
            "https://www.siglaseabreviaturas.com/informatica/page/4/",
            "https://www.siglaseabreviaturas.com/marcas/",
            "https://www.siglaseabreviaturas.com/marcas/page/2/",
            "https://www.siglaseabreviaturas.com/marcas/page/3/",
            "https://www.siglaseabreviaturas.com/marcas/page/4/",
            "https://www.siglaseabreviaturas.com/marcas/page/5/",
            "https://www.siglaseabreviaturas.com/marcas/page/6/",
            "https://www.siglaseabreviaturas.com/internet/",
            "https://www.siglaseabreviaturas.com/internet/page/2/",
            "https://www.siglaseabreviaturas.com/internet/page/3/",
            "https://www.siglaseabreviaturas.com/jogos/",
            "https://www.siglaseabreviaturas.com/jogos/page/2/",
            "https://www.siglaseabreviaturas.com/jogos/page/3/",
            "https://www.siglaseabreviaturas.com/jogos/page/4/"
            ]

    for url in urls:
        get_url_data(result, url)

    print(len(result))

    fp = open("result.txt", "w")
    json.dump(result, fp)

