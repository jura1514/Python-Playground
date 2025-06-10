import json

def write_json_file(data, file_path = "monitor_data.json"):
    """
    Write data to a JSON file.
    
    :param file_path: Path to the JSON file.
    :param data: Data to write to the file.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_json_file(file_path = "monitor_data.json"):
    """
    Read data from a JSON file.
    
    :param file_path: Path to the JSON file.
    :return: Data read from the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {file_path}. Error: {e}")
        return None