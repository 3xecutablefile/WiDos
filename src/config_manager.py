import yaml

CONFIG_PATH = "config.yaml"

def load_config():
    try:
        with open(CONFIG_PATH, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[!] Config file not found: {CONFIG_PATH}")
        return None
    except Exception as e:
        print(f"[!] Error loading config: {e}")
        return None
