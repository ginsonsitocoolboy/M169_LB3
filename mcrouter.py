import requests

def register_mapping(hostname, container_name):
    url = "http://localhost:25564/api/mappings"
    payload = {
        "host": hostname,
        "target": f"{container_name}:25564"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return {"mapping": "added", "host": hostname}
        else:
            return {"mapping_error": response.text}
    except Exception as e:
        return {"mapping_error": str(e)}
