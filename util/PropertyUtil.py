import os
def get_property_string(file_name):
    props = {}
    base_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base_dir, file_name)
    with open(path, "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=")
                props[key.strip()] = value.strip()
    return props