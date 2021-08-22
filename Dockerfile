FROM python:3

COPY ./soundbird.py /opt/soundbird/
COPY ./requirements.txt /opt/soundbird
WORKDIR /opt/soundbird/
RUN mkdir /opt/soundbird/stuff; pip install --no-cache-dir -r /opt/soundbird/requirements.txt
RUN apt update; apt -y install ffmpeg
CMD ["python", "-u", "/opt/soundbird/soundbird.py"]
