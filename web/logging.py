from logging import Formatter, StreamHandler, INFO
from sys import stdout

stream_formatter = Formatter(
    fmt='[{asctime}.{msecs:0<3.0f}] {message}',
    datefmt='%H:%M:%S',
    style='{'
)

stream_handler = StreamHandler(
    stream=stdout
)

stream_handler.setFormatter(stream_formatter)
stream_handler.setLevel(INFO)
