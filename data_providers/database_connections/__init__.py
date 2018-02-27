import os
import inspect

keys_dir = os.path.join(os.path.join(os.path.join(
            os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
                os.pardir), os.pardir), "keys")

mysql_key_path = os.path.join(keys_dir, "mysql_key.json")