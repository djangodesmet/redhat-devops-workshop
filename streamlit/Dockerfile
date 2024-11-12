FROM # TODO: image

WORKDIR /home/jovyan/devops-course-basic

COPY ./streamlit/requirements.txt ./streamlit/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ./streamlit/requirements.txt

COPY ./streamlit ./streamlit
