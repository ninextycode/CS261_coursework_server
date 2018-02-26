import inspect, os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
        os.path.join(os.path.join(
            os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
                os.pardir), os.pardir), "keys/google_key.json")
