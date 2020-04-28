import os
import requests
import argparse
from bs4 import BeautifulSoup

CURRENT_INDEX = 0
BASE_LINK = 'https://link.springer.com'
TITLES = {'pdf': 'Download this book in PDF format',
          'epub': 'Download this book in EPUB format'}
CHUNK_SIZE = 2000


def get_title(soup):
    global CURRENT_INDEX
    try:
        return soup.find('h1').text
    except:
        title = "Documento_{}".format(CURRENT_INDEX)
        CURRENT_INDEX += 1
        return title


def get_link(soup, doc_format='pdf'):
    try:
        return soup.find('a', {'title': TITLES[doc_format]})['href'], doc_format
    except:
        try:
            alt_doc_format = 'pdf' if doc_format == 'epub' else 'pdf'
            print("Se cambio el formato desde {} a {}".format(
                doc_format, alt_doc_format))
            return soup.find('a', {'title': TITLES[alt_doc_format]})['href'], alt_doc_format
        except:
            return None, None


def download_pdf_from_link(link, doc_format):
    print("Link:", link)
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = get_title(soup).replace("/", "-")
    print("Title:", title)

    link, final_format = get_link(soup, doc_format)
    filepath = "{}.{}".format(title, final_format)

    if os.path.exists(filepath):
        print("Ya existe")
        print("#####################")
        return
    if link is None:
        print("NO SE PUDO DESCARGAR")
        print("#####################")
        return

    link = BASE_LINK + link
    pdf = requests.get(link, stream=True)
    print("Descargando")
    with open(filepath, 'wb') as fd:
        for chunk in pdf.iter_content(CHUNK_SIZE):
            fd.write(chunk)
    print("Guardado")
    print("#####################")


def main(doc_links, doc_format):
    with open(doc_links) as f:
        links = f.readlines()
    for raw_link in links:
        link = raw_link.strip()
        download_pdf_from_link(link, doc_format)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument(
        '--doc_links',
        type=str,
        help="""\
        Ruta al documento con links.\
        """,
        required=True
    )
    PARSER.add_argument(
        '--doc_format',
        type=str,
        help="""\
        Formato preferido. Opciones: pdf, epub.
        """,
        default='pdf'
    )
    FLAGS = PARSER.parse_args()
    main(FLAGS.doc_links, FLAGS.doc_format)
