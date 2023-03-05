
from pathlib import Path
import shutil

image_extensions = ('JPEG', 'PNG', 'JPG', 'SVG')
video_extensions = ('AVI', 'MP4', 'MOV', 'MKV')
document_extensions = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
music_extensions = ('MP3', 'OGG', 'WAV', 'AMR')
archive_extensions = ('ZIP', 'GZ', 'RAR')

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
    Image_list = []
    video_list = []
    music_list = []
    unknown_list = []

    for i in p.iterdir():
        if i.name == 'Images':
            for j in i.iterdir():
                if j.name.split('.')[-1] not in list_of_all:
                    list_of_all.append(j.name.split('.')[-1])
                Image_list.append(j.name)
        if i.name == 'Videos':
            for j in i.iterdir():
                if j.name.split('.')[-1] not in list_of_all:
                    list_of_all.append(j.name.split('.')[-1])
                video_list.append(j.name)
        if i.name == 'Documents':
            for j in i.iterdir():
                if j.name.split('.')[-1] not in list_of_all:
                    list_of_all.append(j.name.split('.')[-1])
                Image_list.append(j.name)
        if i.name == 'Music':
            for j in i.iterdir():
                if j.name.split('.')[-1] not in list_of_all:
                    list_of_all.append(j.name.split('.')[-1])
                music_list.append(j.name)
        if i.name == 'Unknown':
            for j in i.iterdir():
                if j.name.split('.')[-1] not in list_of_all:
                    list_of_all.append(j.name.split('.')[-1])
                unknown_list.append(j.name)
    if list_of_all:
        print(f'List of extension: {list_of_all}')
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
        shutil.move(item, destination)
    except shutil.Error as i:
        print(i)


def normalize(p):
    # функція для перейменування файлів
    for item in p.iterdir():
        if item.is_file():
            a = (item.name.split('.')[0]).translate(TRANS)
            b = item.name.split('.')[-1]
            new_filename = a + '.' + b
            new_file_path = p / new_filename
            Path.rename(item, new_file_path)
        elif item.is_dir():
            normalize(item)


def unpuckarhives(p):
    for item in p.iterdir():
        extension = item.name.split('.')[-1].upper()
        if extension in archive_extensions:
            # перемістити файл в папку з архівами
            try:
                shutil.unpack_archive(item, (p / item.name.split('.')[0]))
                my_file = Path(item)
                my_file.unlink()
            except shutil.ReadError as i:
                print(i)

        elif item.is_dir():
            unpuckarhives(item)


# функція для сортування файлів та папок
def sort_folder(path):
    p = Path(path)
    unpuckarhives(p)
    for item in p.iterdir():
        global s
        if item.is_file():
            extension = item.name.split('.')[-1].upper()

            if extension in image_extensions:
                # перемістити файл в папку з зображеннями
                destination = Path(s) / 'Images'
                moving_file(destination, item)
            elif extension in video_extensions:
                # перемістити файл в папку з відео
                destination = Path(s) / 'Videos'
                moving_file(destination, item)
            elif extension in document_extensions:
                # перемістити файл в папку з документами
                destination = Path(s) / 'Documents'
                moving_file(destination, item)
            elif extension in music_extensions:
                # перемістити файл в папку з музикою
                destination = Path(s) / 'Music'
                moving_file(destination, item)

                # перемістити файл в папку з невідомими розширеннями
            else:
                destination = Path(s) / 'Unknown'
                moving_file(destination, item)

        elif item.is_dir():
            sort_folder(item)

    for folder in p.iterdir():
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
    normalize(p)
    lists_of_result(p)


if __name__ == '__main__':
    import sys
    s = sys.argv[1]
    sort_folder(s)
