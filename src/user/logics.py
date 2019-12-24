import os


def save_avatar(nickname, avatar_file):
    base_dir = os.path.dirname(os.path.abspath(__name__))
    file_path = os.path.join(base_dir, 'static', 'upload', nickname)
    avatar_file.save(file_path)
