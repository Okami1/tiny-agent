import os

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
    }
]



def list_dir(path) -> list[str] | str:
    try:
        return os.listdir(path)
    except Exception as e:  # noqa: BLE001
        return str(e)
