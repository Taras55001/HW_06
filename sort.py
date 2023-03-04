
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
            new_filename = p / (a + '.' + b)
            Path.rename(item, new_filename)
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


if __name__ == '__main__':
    import sys
    s = sys.argv[1]
    sort_folder(s)
