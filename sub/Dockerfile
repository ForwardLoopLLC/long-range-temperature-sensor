FROM library/python:3.6
RUN pip install matplotlib paho-mqtt
WORKDIR /sub
ENV DISPLAY=:1
CMD python -u /sub/main.py
