# Use the image below with all packages pre-installed to speedup the build
FROM python:3

# Set the working directory from which the next commands are executed
WORKDIR .

# Transfer the requirement file first to allow layered caching
COPY ./api/requirements.txt ./api/requirements.txt

# Use no-cache-dir to avoid storing cache in the docker image
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ./api/requirements.txt

# Transfer the api folder to the docker image
COPY ./api ./api
