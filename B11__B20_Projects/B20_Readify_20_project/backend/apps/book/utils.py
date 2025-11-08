from .models import Book, Chapter
import requests


def load_book_from_openlibrary(olid):
    url = f"https://openlibrary.org/books/{olid}.json"
    r = requests.get(url)
    data = r.json()

    title = data.get('title', olid)
    author = data.get('authors', [{'name': 'Unknown'}])[0]['name']

    book = Book.objects.create(title=title, author=author)

    txt_url = "https://www.gutenberg.org/files/1342/1342-0.txt"
    r = requests.get(txt_url)
    text = r.text

    chapter_number = 0
    chapter_text = ""
    for line in text.splitlines():
        line = line.strip()
        if line.lower().startswith("chapter"):
            if chapter_text:
                Chapter.objects.create(
                    book=book,
                    number=chapter_number,
                    title=f"Глава {chapter_number}",
                    text=chapter_text
                )
                chapter_text = ""
            chapter_number += 1
        else:
            chapter_text += line + "\n"

    if chapter_text:
        Chapter.objects.create(
            book=book,
            number=chapter_number,
            title=f"Глава {chapter_number}",
            text=chapter_text
        )

    book.total_chapters = chapter_number
    book.save()
    return book
