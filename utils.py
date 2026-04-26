import os
import niquests
from datetime import datetime

from sqlalchemy import UUID

from session import db_host


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


def dir_scan(path) -> list[str]:
    """Сканируем подпапки в папке"""
    result = []
    for item in os.scandir(path):
        if item.is_dir():
            result.append(item.name)
    return result


def now_formated():
    return datetime.now().date().strftime("%Y-%m-%d")


def request_cards(category_id, all=False) -> list[dict[str, str]]:
    request = niquests.get(f'http://{db_host}:8080/api/cards?categoryId={str(category_id)}&all={all}')
    return request.json()


def get_first_category_id() -> UUID:
    request = niquests.get(f'http://{db_host}:8080/api/categories/ids')
    return request.json()[0]