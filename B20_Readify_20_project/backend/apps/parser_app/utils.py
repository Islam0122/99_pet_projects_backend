import re

def split_into_chapters(text):
    """
    Разделяем книгу на главы по шаблону 'Глава X'
    """
    chapters = re.split(r'(?:Глава)\s+(\d+)', text, flags=re.IGNORECASE)
    result = []
    for i in range(1, len(chapters), 2):
        number = int(chapters[i])
        content = chapters[i + 1].strip()
        result.append({"number": number, "content": content})
    return result

def find_chapter_by_number(text, number):
    chapters = split_into_chapters(text)
    for ch in chapters:
        if ch["number"] == number:
            return ch["content"]
    return None
