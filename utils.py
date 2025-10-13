import os


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


def dir_scan(path)-> list[str]:
    """Сканируем подпапки в папке"""
    result = []
    for item in os.scandir(path):
        if item.is_dir():
           result.append(item.name)
    return result