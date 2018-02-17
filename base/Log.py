import datetime


def log(*message):
    print(datetime.datetime.now(), "\t", *message)
