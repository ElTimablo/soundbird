FROM python:3

WORKDIR /opt/soundbird/
COPY ./requirements.txt /opt/soundbird
RUN mkdir /opt/soundbird/stuff; pip install --no-cache-dir -r /opt/soundbird/requirements.txt
RUN apt update; apt -y install ffmpeg
COPY ./soundbird.py /opt/soundbird/
CMD ["python", "-u", "/opt/soundbird/soundbird.py"]
