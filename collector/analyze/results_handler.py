import os
from django.conf import settings


class Results:
    def __init__(self, result_file_paths=None):
        self.result_file_paths = result_file_paths

    def fake_create_results_files(self, prefix):
        """Creating fake dict (with filename: file_path values) for testing result uploader"""
        folder = os.path.join(settings.MEDIA_ROOT, '_results')
        os.makedirs(folder, exist_ok=True)
        files = ['_result.mp4']
        for file in files:
            file_name = prefix+file
            file_path = os.path.join(folder, file_name)
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write('test_video')
                self.result_file_paths[file_name] = os.path.abspath(file_path)

    def get_results_file_paths(self, prefix):
        if not self.result_file_paths.get('_results.mp4'):
            self.fake_create_results_files(prefix)
        # print(self.result_file_paths)
        return self.result_file_paths
