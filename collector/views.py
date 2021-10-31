# from django.core.validators import URLValidator
# from django.core.exceptions import ValidationError
import asyncio
from django.http import JsonResponse

from .models import Recognize
from .loader import download_file, get_loop, UploaderToCloud
from .analyze.analyser import Analyser

def post_recognize(request):
    if request.method == 'POST':
        source, prefix = request.POST.get('source'), request.POST.get('prefix')
        # validate = URLValidator(schemes=['HTTPS'], verify_exists=True)
        # try:
        #     print(validate(source))
        # except Exception as e:
        #     print(e)
        #     return JsonResponse({'code': e})
        if not Recognize.objects.filter(prefix=prefix).count():
            record = Recognize(source=source, prefix=prefix)
            record.save()
            res = {'code': 200, 'message': 'OK'}
            download_file(source, prefix)
            analyser = Analyser(prefix)
            result_file_paths = analyser.run_pipeline()

            uploader = UploaderToCloud()
            loop = get_loop()
            if loop.is_running():
                print('loop has already been running!')
                loop.run_in_executor(None, uploader.save_to_cloud, prefix, result_file_paths)
            else:
                print('loop has just started!')
                asyncio.run(uploader.save_to_cloud(prefix, result_file_paths))
        else:
            res = {'code': 409, 'message': f'Conflict: URL with {prefix = } has already been sent to recognizer!'}
        return JsonResponse(res)
