import json
import os
from django.conf import settings
from .file_handler import extract_audio_from_clip, split_video_file
from .embeds import create_embeds, save_pretrained_audio_model


class Analyser:
    def __init__(self, prefix):
        self.prefix = prefix
        self.results = {}
        self.result_file_paths = {}

    def extract_audio(self):
        filename = self.prefix + '.mp4'
        extract_audio_from_clip(filename)

    def extract_video(self):
        pass

    def analyze_audio(self):
        save_pretrained_audio_model()
        # create_embeds(self.prefix)
        audio_result_dict = {'result': [{'time_start': 3.12, 'time_end': 4.15}]}
        audio_result_json = json.dumps(audio_result_dict)
        self.results['audio'] = audio_result_json

    def split_video(self):
        filename = self.prefix + '.mp4'
        split_video_file(filename)

    def analyze_video(self):
        video_result_dict = {'result':
            [
                {'time_start': 2.12,
                 'time_end': 3.41,
                 'corner_1': [123, 456],
                 'corner_2': [321,654]},
                {'time_start': 2.12,
                 'time_end': 3.41,
                 'corner_1': [123, 456],
                 'corner_2': [321, 654]},
            ]
        }
        video_result_json = json.dumps(video_result_dict)
        self.results['video'] = video_result_json

    def collect_results_to_files(self):
        folder = os.path.join(settings.MEDIA_ROOT, '_results')
        os.makedirs(folder, exist_ok=True)
        file_name_parts = {'_audio.json': 'audio', '_video.json': 'video'}
        for file in file_name_parts:
            file_name = self.prefix + file
            file_path = os.path.join(folder, file_name)
            tag = file_name_parts.get(file)
            with open(file_path, 'w') as f:
                f.write(self.results.get(tag))
            self.result_file_paths[file_name] = os.path.abspath(file_path)

    def run_pipeline(self):
        self.extract_audio()
        self.extract_video()
        self.analyze_audio()
        # self.split_video()
        self.analyze_video()
        self.collect_results_to_files()
        return self.result_file_paths
