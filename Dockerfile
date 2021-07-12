FROM python:3

COPY ./ /opt/dumbot/
WORKDIR /opt/dumbot/
RUN pip install --no-cache-dir -r /opt/dumbot/requirements.txt
RUN apt update; apt -y install ffmpeg
CMD ["python", "/opt/dumbot/dumbot.py"]
