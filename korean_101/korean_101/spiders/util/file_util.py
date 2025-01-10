import re
import json

DEFAULT_DOWNLOAD_FOLDER = "./files"


def extract_pdf_file_name_from_url(url):
    # Find the position of the last slash
    last_slash_pos = url.rfind('/')

    # Extract everything after the last slash
    file_with_query = url[last_slash_pos + 1:]

    # Find the position of the first question mark
    question_mark_pos = file_with_query.find('?')

    # If there's no question mark, return the whole file_with_query
    if question_mark_pos == -1:
        return file_with_query
    else:
        # Return only up to the point just before the question mark
        return file_with_query[:question_mark_pos]


def clean_title(title):
    # Chuyển tất cả chữ cái thành chữ thường
    title = title.lower()

    # Thay thế các ký tự không phải chữ cái, số, hoặc gạch dưới bằng khoảng trắng
    title = re.sub(r'[^a-z0-9\s]', '', title)

    # Thay thế các ký tự space và tab bằng '_'
    title = re.sub(r'[\s]+', '_', title)

    # Trả về title đã xử lý
    return title


def to_json(file_name, data):
    with open(file_name, 'w', encoding="utf-8") as file:
        json.dump(data.to_dict(), file, ensure_ascii=False, indent=4)
