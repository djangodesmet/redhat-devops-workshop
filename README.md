
# Redhat OpenShift AI

## General Setup

Make sure you work in a workbench that has a data connection to the s3 bucket provided by Redhat. This bucket contains the Gliner model files.

## Run the API locally

Install requirements:
```sh
pip install -r requirements.txt
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

## Run the API remotely

### (Optional) registering the model

There should be a model already registered in the model registry but if you want to register a new model you can do this through the OpenShift AI dashboard by clicking `Model Registry` and then clicking `Register model`. Make sure you point to the correct model file.

For this project there is a registered model called `gliner-multi`.


### Deploying the model

First, initialize a model serving platform through the RHOAI dashboard by going to your data science project overview page and clicking on `Models`. From there, click on `Multi-model serving platform`. Make sure you tick the box to create a `Route` and tick the box to create a `Token`. Choose the OpenVino model server and onnx runtime. Make sure you point to the correct model file.

### Call the remote model API

You can call the remote model by running:
```sh
export ENDPOINT=<YOUR_MODEL_ENDPOINT>
export TOKEN=<YOUR_API_TOKEN>
python -m api.call_endpoint --local=False
```

Both the endpoint and the token can be obtained through the RHOAI dashboard.

Due to the way the model is served through the RHOAI dashboard, the API expects some complex inputs. There should be a possibility to add some custom code to the API endpoint that can take care of pre and postprocessing but until that is implemented, I have provided some example data via the `get_data` function. This is also why the returned output is just numbers and not converted back to text as we are used to with the Gliner package.

## Streamlit

### Run streamlit app locally

Start the streamlit app:
```sh
streamlit run streamlit/main/app.py --server.enableCORS=false
```

### Run streamlit app remotely

The only thing that is needed in this repository to deploy the streamlit application remotely is a `run` file inside a `.s2i/bin` folder. No need to write a Dockerfile and build an image, the OpenShift platform will do this for us. The `run` file will be read by the Build functionality of the OpenShift platform. Next to that, it will take in the contents of `pyproject.toml` and install the packages specified in there. 

In order to deploy the application, go to the OpenShift console and make sure you are on the `Developer` view. From there click `+Add` and choose `Import from Git`. Paste the https git clone url into the field. Under the advanced git options you can optionally specify which branch to build from. Under `Build` and advanced build options, add an environment variable from Secret. Select `default-name-multi-model-server-sa` and then `token` and name it `SVA_TOKEN`. Add another environment variable and call it `REMOTE` and give it the value `True`. Add another environment variable and call it `ENDPOINT` and paste the inference endpoint into the value field.

Under `Deploy` and `Resource type` choose `Deployment`. Set `Target port` to 8080. 

Click deploy and wait a few minutes for the application to start running. You can get the url for the application by clicking on `Topology` and clicking on the deployment. The url is under the `Routes` section.
