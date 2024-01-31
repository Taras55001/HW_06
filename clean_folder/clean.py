'''script for sorting and cleaning files and folders'''
from pathlib import Path
import shutil
import sys

image_extensions = ('.JPEG', '.PNG', '.JPG', '.SVG')
video_extensions = ('.AVI', '.MP4', '.MOV', '.MKV')
document_extensions = ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX')
music_extensions = ('.MP3', '.OGG', '.WAV', '.AMR')
archive_extensions = ('.ZIP', '.GZ', '.RAR')

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def creating_folders(destination):
    if not destination.exists():
        destination.mkdir()


def lists_of_result(p):
    list_of_all = []
    documents_list = []
    Image_list = []
    video_list = []
    music_list = []
    unknown_list = []
    for i in p.glob('**/*.*'):
        if i.suffix.upper() not in list_of_all:
            list_of_all.append(i.suffix.upper())

    for i in p.glob('**/*.*'):
        if i.parent == p/'Images':
            Image_list.append(i.stem)
        elif i.parent == p/'Videos':
            video_list.append(i.stem)
        elif i.parent == p/'Documents':
            documents_list.append(i.stem)
        elif i.parent == p/'Music':
            music_list.append(i.stem)
        elif i.parent == p/'Unknown':
            unknown_list.append(i.stem)

    if list_of_all:
        print(f'List of extension: {list_of_all}')
    if documents_list:
        print(f'Files in Documents: {documents_list}')
    if Image_list:
        print(f'Files in Images: {Image_list}')
    if video_list:
        print(f'Files in Videos: {video_list}')
    if music_list:
        print(f'Files in Music: {music_list}')
    if unknown_list:
        print(f'Files in Unknown: {unknown_list}')


def moving_file(destination, item):
    creating_folders(destination)
    try:
        item.replace(destination/item.name)
    except shutil.Error as i:
        print(i)


def normalize(p):
    # функція для перейменування файлів
    for item in p.glob('**/*.*'):
        if item.is_file():
            a = item.stem.translate(TRANS)
            b = item.suffix
            new_filename = a + b
            item.rename(item.parent / new_filename)


# перемістити файл в папку з архівами
def unpuckarhives(p):
    for item in p.glob('**/*.*'):
        try:
            if item.name.split('.')[-1].upper() in archive_extensions:
                shutil.unpack_archive(
                    item, (p / item.name.split('.')[0]))
                item.unlink()
        except shutil.ReadError as i:
            print(i)


# функція для сортування файлів та папок
def sort_folder(path):
    p = Path(path)
    unpuckarhives(p)
    for item in p.glob('**/*.*'):
        if item.is_file():
            if item.suffix.upper() in image_extensions:
                # перемістити файл в папку з зображеннями
                destination = p / 'Images'
                moving_file(destination, item)
            elif item.suffix.upper() in video_extensions:
                # перемістити файл в папку з відео
                destination = p / 'Videos'
                moving_file(destination, item)
            elif item.suffix.upper() in document_extensions:
                # перемістити файл в папку з документами
                destination = p / 'Documents'
                moving_file(destination, item)
            elif item.suffix.upper() in music_extensions:
                # перемістити файл в папку з музикою
                destination = p / 'Music'
                moving_file(destination, item)
                # перемістити файл в папку з невідомими розширеннями
            else:
                destination = p / 'Unknown'
                moving_file(destination, item)

        elif item.is_dir():
            sort_folder(item)

    for folder in p.iterdir():
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
    normalize(p)
    lists_of_result(p)


def main():
    try:
        s = sys.argv[1]
        sort_folder(s)
    except IndexError:
        print('Something went wrong')

if __name__ is "__main__":
    main()