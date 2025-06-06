# install.py
import os
import sys
import shutil
from huggingface_hub import hf_hub_download, login

def download_if_missing(repo_id, filename, cache_dir):
    """Download a file from HF if not already in cache_dir."""
    local_path = os.path.join(cache_dir, filename)
    if not os.path.exists(local_path):
        print(f"Downloading {filename} from {repo_id}...")
        try:
            path = hf_hub_download(repo_id=repo_id, filename=filename, cache_dir=cache_dir)
            # hf_hub_download returns cache path (not our desired path), so copy it:
            shutil.copy(path, local_path)
            print(f"Saved {filename} to {local_path}")
        except Exception as e:
            print(f"Error downloading {filename}: {e}\n" +
                  f"Ensure you have access or run `huggingface-cli login` for private repos.")
            raise
    return local_path

def install():
    ext_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(ext_dir, "t5xxl_data")
    os.makedirs(data_dir, exist_ok=True)
    repo_id = "Kaoru8/T5XXL-Unchained"
    # Optional: use env var or prompting login for token
    hf_token = os.environ.get("HUGGINGFACE_TOKEN")
    if hf_token:
        login(token=hf_token)
    try:
        # Download tokenizer.json, config.json, and the safetensors checkpoint (f16)
        download_if_missing(repo_id, "tokenizer.json", data_dir)
        download_if_missing(repo_id, "config.json", data_dir)  # t5_config_xxl.json was renamed
        download_if_missing(repo_id, "t5xxl-unchained-f16.safetensors", data_dir)
    except Exception:
        print("Failed to download T5XXL-Unchained model files. Exiting.")
        sys.exit(1)
    print("T5XXL-Unchained model downloaded successfully.")

if __name__ == "__main__":
    install()
