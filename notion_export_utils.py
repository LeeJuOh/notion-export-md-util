import logging
import os
import sys
from typing import Dict, List
import zipfile
from collections import defaultdict


def create_looger() -> logging.Logger:
    logger = logging.getLogger("my")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s -  %(levelname)s - %(message)s')
    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    logger.addHandler(stream_hander)

    return logger


def init_path() -> str:
    global logger

    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        os.chdir(application_path)
        logger.info(f"chdir: {application_path}")
        return application_path
    else:
        return os.getcwd()

def find_zip_files(dir: str, zip_files: Dict[str, List[str]]) -> None:
    global logger

    try:
        files = os.listdir(dir)
        for file in files:
            full_filename = os.path.join(dir, file)
            if os.path.isdir(full_filename):
                find_zip_files(full_filename, zip_files)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.zip':
                    zip_files[dir].append(full_filename)
                    logger.info(f"target file: {full_filename}")
    except PermissionError as e:
        logger.error(e)


def extract_zip_file_with_renaming(path: str, zip_file: str, image_files: Dict[str, List[str]]) -> None:
    global logger

    with zipfile.ZipFile(zip_file, 'r') as zip_obj:
        image_idx = 1
        files = []
        for idx, full_filename in enumerate(zip_obj.namelist()):
            file_name, ext = os.path.splitext(full_filename)
            image_path = os.path.join(path, "image")
            if idx == 0:
                save_file_name = '_'.join(file_name.split()[:-1])
                create_directory(image_path)

            if ext == '.md':
                save_path = f"{os.path.join(path, save_file_name)}{ext}"
            elif ext in ('.png', '.jpeg', '.jpg'):
                save_path = f"{os.path.join(image_path, str(image_idx))}{ext}"
                image_files[f"{os.path.join(path, save_file_name)}.md"].append(save_path)
                image_idx += 1
            else:
                continue
            with open(save_path, "wb") as f:
                f.write(zip_obj.read(full_filename))
                logger.info(f"extract path: {save_path}")


def create_directory(path: str) -> None:
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            logger.info(f"create directorty: {path}")
    except OSError:
        logger.error(f"Error: Creating directory. {path}")


def remove_zip_file(zip_file):
    global logger

    if os.path.isfile(zip_file):
        logger.info(f"remove zip file: {zip_file}")
        os.remove(zip_file)
    else:
        logger.warning(f"not file type: {zip_file}")


def update_image_path(md_file: str, images: List[str]):
    global logger, search_dir_path

    with open(md_file, 'r+') as f:
        idx = 0
        lines = []
        try:
            for line in f:
                if line.lstrip().startswith('!['):
                    image_path = images[idx].replace(search_dir_path, '..')
                    new_line = f'![image_{idx + 1}]({image_path})\n'
                    logger.info(f"update image url: {new_line[:-1]}")
                    lines = lines + [new_line]
                    idx += 1
                else:
                    lines = lines + [line]
        except IndexError as e:
            logger.error(f"index error: {idx}, {line}")
        f.seek(0)               # file pointer 위치를 처음으로 돌림
        f.writelines(lines)     # 수정한 lines를 파일에 다시 씀
        f.truncate()


if __name__ == '__main__':
    logger = create_looger()
    logger.info("start")
    search_dir_path = init_path()
    zip_files = defaultdict(list)
    image_files = defaultdict(list)
    logger.info(f"find dir: {search_dir_path}")

    find_zip_files("./test", zip_files)
    print(zip_files)
    for path, zip_files in zip_files.items():
        for zip_file in zip_files:
            extract_zip_file_with_renaming(
                path,
                zip_file,
                image_files
            )
            remove_zip_file(zip_file)
    for md_file, images in image_files.items():
        update_image_path(md_file, images)
    logger.info("finish")
