import os
import requests
from tqdm import tqdm


def save_pretrained_audio_model():
    os.makedirs('media/models/', exist_ok=True)
    res_path = 'media/models/audio_model.pt'
    # model_url = 'https://dl.fbaipublicfiles.com/fairseq/wav2vec/wav2vec_small_10m.pt' # small
    model_url = 'https://dl.fbaipublicfiles.com/fairseq/wav2vec/w2v_large_lv_fsh_swbd_cv_ftls960.pt' # big
    downloaded_fz = int(requests.get(model_url, stream=True).headers['Content-length'])
    print(f'{downloaded_fz = } bytes')
    if os.path.exists(res_path):
        file_on_dick_fz = os.stat(res_path).st_size
        print(f'{file_on_dick_fz = } bytes')
    if (not os.path.exists(res_path) or
        (os.path.exists(res_path) and downloaded_fz != file_on_dick_fz)):

        print('Started downloading a big model!')
        resp = requests.get(model_url,
                            verify=False, stream=True)
        with open(res_path, 'wb') as f:
            for block in tqdm(resp.iter_content(1024)):
                f.write(block)

def create_embeds():
    import torch
    import fairseq
    model_path = 'media/models/audio_model.pt'
    model, cfg, task = fairseq.checkpoint_utils.load_model_ensemble_and_task([model_path])
    model = model[0]
    model.eval()

    wav_input_16khz = torch.randn(1,10000)
    z = model.feature_extractor(wav_input_16khz)
    c = model.feature_aggregator(z)