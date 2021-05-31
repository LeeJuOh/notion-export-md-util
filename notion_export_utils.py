import logging
import os
import sys
import zipfile
from collections import defaultdict


def create_looger():
    logger = logging.getLogger("my")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s -  %(levelname)s - %(message)s')
    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(formatter)
    logger.addHandler(stream_hander)

    return logger


def init_path():
    global logger

    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        os.chdir(application_path)
        logger.info(f"chdir: {application_path}")
        return application_path
    else:
        return os.getcwd()

def search_zip_files(search_dir_path, zip_files_by_dir_path):
    global logger

    try:
        files = os.listdir(search_dir_path)
        for file in files:
            full_filename = os.path.join(search_dir_path, file)
            if os.path.isdir(full_filename):
                search_zip_files(full_filename, zip_files_by_dir_path)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.zip':
                    zip_files_by_dir_path[search_dir_path].append(full_filename)
                    logger.info(f"target file: {full_filename}")
    except PermissionError as e:
        logger.error(e)


def extract_zip_file_with_renaming(dir_path, zip_file, image_files_by_md_file):
    global logger, image_dir_path

    with zipfile.ZipFile(zip_file, 'r') as zip_obj:
        image_idx = 1
        for idx, full_filename in enumerate(zip_obj.namelist()):
            file_name, ext = os.path.splitext(full_filename)
            if idx == 0:
                print(file_name.split())
                valid_file_name = ''.join(file_name.split()[:-1])

            if ext == '.md':
                save_path = f"{os.path.join(dir_path, valid_file_name)}{ext}"
                image_files_by_md_file.setdefault(save_path, [])
            elif ext in ('.png', '.jpeg', '.jpg'):
                save_path = f"{os.path.join(image_dir_path, valid_file_name)}_{image_idx}{ext}"
                image_files_by_md_file[f"{os.path.join(dir_path, valid_file_name)}.md"].append(save_path)
                image_idx += 1
            else:
                continue
            with open(save_path, "wb") as f:
                f.write(zip_obj.read(full_filename))
                logger.info(f"extract path: {save_path}")


def remove_zip_file(zip_file):
    global logger

    if os.path.isfile(zip_file):
        logger.info(f"remove zip file: {zip_file}")
        os.remove(zip_file)
    else:
        logger.warning(f"not file type: {zip_file}")


def update_image_path(md_file, image_files):
    global logger, search_dir_path

    with open(md_file, 'r+') as f:
        idx = 0
        lines = []
        for line in f:
            if line.lstrip().startswith('!'):
                image_path = image_files.pop(0).replace(search_dir_path, '..')
                new_line = f'![image_{idx}]({image_path})\n'
                logger.info(f"update image url: {new_line[:-1]}")
                lines = lines + [new_line]
            else:
                lines = lines + [line]
        f.seek(0)               # file pointer 위치를 처음으로 돌림
        f.writelines(lines)     # 수정한 lines를 파일에 다시 씀
        f.truncate()


if __name__ == '__main__':
    logger = create_looger()
    logger.info("start")
    search_dir_path = init_path()
    image_dir_path = os.path.join(search_dir_path, 'image')
    zip_files_by_dir_path = defaultdict(list)
    image_files_by_md_file = defaultdict(list)
    logger.info(f"search dir: {search_dir_path}")
    logger.info(f"image dir: {image_dir_path}")

    search_zip_files(search_dir_path, zip_files_by_dir_path)
    for dir_path, zip_files in zip_files_by_dir_path.items():
        for zip_file in zip_files:
            extract_zip_file_with_renaming(
                dir_path,
                zip_file,
                image_files_by_md_file
            )
            remove_zip_file(zip_file)
    for md_file, image_files in image_files_by_md_file.items():
        update_image_path(md_file, image_files)
    logger.info("finish")
