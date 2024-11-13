# Running API locally

Install requirements:
```sh
pip install -r requirements-new.txt
```

Download model:
```sh
python api/download_model.py
```

Start API:
```sh
python api/api.py
```

Calling API locally:
```sh
python api/call_endpoint.py --local=True
```

# Remote API

Get token from `huggingface-models` model server and put this in `token = ""` in `api/inference.py`

Calling remote API:
```sh
python api/inference.py
```
