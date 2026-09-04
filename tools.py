import os
import requests

tools = [
    {
        "name": "list_dir",
        "description": "List the contents of a directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path of the directory to list.",
                }
            },
            "required": ["path"],
        },
    },
    {
        "name": "read_file",
        "description": "Read the contents of a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path of the file to read.",
                }
            },
            "required": ["path"],
        },
    },
    {
        "name": "fetch_url",
        "description": "Fetch the contents of a URL.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to fetch.",
                }
            },
            "required": ["url"],
        },
    }
]



def list_dir(path) -> list[str] | str:
    try:
        return os.listdir(path)
    except Exception as e:  # noqa: BLE001
        print(f"Error listing directory {path}: {e}")
        return str(e)


def read_file(path) -> str:
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:  # noqa: BLE001
        print(f"Error reading file {path}: {e}")
        return str(e)


def fetch_url(url) -> str:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text
    except Exception as e:  # noqa: BLE001
        print(f"Error fetching URL {url}: {e}")
        return str(e)