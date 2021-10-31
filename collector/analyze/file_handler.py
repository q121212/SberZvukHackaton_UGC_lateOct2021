import math
import os
import shlex
import subprocess
from django.conf import settings


def get_video_length(filename):
    file_path = os.path.join(settings.BASE_DIR, f'media/{filename}')
    print(file_path)
    split_command = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 '
    output = subprocess.check_output(split_command + file_path,
                                     stderr=subprocess.STDOUT, shell=True).strip()

    video_length = int(float(output))
    print("Video length in seconds: " + str(video_length))

    return video_length


def split_video_file(filename, split_len=1):
    assert split_len and split_len > 0, f'{split_len = }, but should be > 0'
    video_len = get_video_length(filename)
    split_cnt = int(math.ceil(video_len / float(split_len)))

    if split_cnt == 1:
        print("Video length is less then the target split length.")

    vcodec, acodec, extra = "copy", "copy", ''
    split_cmd = ["ffmpeg", "-i", os.path.join(settings.BASE_DIR, f'media/{filename}'), "-vcodec", vcodec, "-acodec", acodec] + shlex.split(extra)
    try:
        filebase = ".".join(filename.split(".")[:-1])
        fileext = filename.split(".")[-1]
    except IndexError as e:
        raise IndexError("No `.` in filename. Error: " + str(e))
    for n in range(0, split_cnt):
        split_args = []
        if n == 0:
            split_start = 0
        else:
            split_start = split_len * n

        splitted_folder = os.path.join(settings.BASE_DIR, f'media/splitted/')
        os.makedirs(splitted_folder, exist_ok=True)
        split_args += ["-ss", str(split_start), "-t", str(split_len),
                       f'{splitted_folder}{filebase + "-" + str(n + 1) + "-of-" + str(split_cnt) + "." + fileext}']
        print("About to run: " + " ".join(split_cmd + split_args))
        subprocess.check_output(split_cmd + split_args)


def extract_audio_from_clip(filename):
    file_path = os.path.join(settings.BASE_DIR, f'media/{filename}')
    os.makedirs('media/audio/', exist_ok=True)
    result_file_path = os.path.join(settings.BASE_DIR, f'media/audio/{filename.split(".")[0]}.wav')
    command = f"ffmpeg -i {file_path} -ab 160k -ac 2 -ar 44100 -vn {result_file_path} -y"
    subprocess.call(command, shell=True)