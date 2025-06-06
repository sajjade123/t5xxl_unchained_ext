# scripts/t5_changer.py
import os
import torch
from modules import shared
import modules.script_callbacks as script_callbacks
from transformers import AutoTokenizer, T5EncoderModel, logging
from huggingface_hub import hf_hub_download

# Suppress transformers warnings
logging.set_verbosity_error()

def load_t5_model(repo_id):
    """Load T5 tokenizer and encoder (from HF cache if possible)."""
    # Use local cache folder from install.py
    ext_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(ext_dir, "t5xxl_data")
    # Confirm files exist:
    tok_path = os.path.join(data_dir, "tokenizer.json")
    cfg_path = os.path.join(data_dir, "config.json")
    model_path = os.path.join(data_dir, "t5xxl-unchained-f16.safetensors")
    if not os.path.exists(tok_path) or not os.path.exists(cfg_path) or not os.path.exists(model_path):
        raise FileNotFoundError("T5XXL files not found. Run install script or check downloads.")
    # Load tokenizer and model from local files
    tokenizer = AutoTokenizer.from_pretrained(data_dir, use_fast=True)
    encoder = T5EncoderModel.from_pretrained(data_dir, config=data_dir)
    return tokenizer, encoder

def replace_with_t5(sd_model):
    """Callback to replace text encoder on model load."""
    if not shared.opts.extensions_state.get("t5xxl_unchained_ext.enable", True):
        print("[T5XXL] Extension disabled; skipping T5 replacement.")
        return
    print("[T5XXL] Replacing CLIP with T5XXL-Unchained text encoder...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    try:
        tokenizer, encoder = load_t5_model(shared.opts.extensions_state.get("t5xxl_unchained_ext.repo_id", "Kaoru8/T5XXL-Unchained"))
    except Exception as e:
        print(f"[T5XXL] Error loading model/tokenizer: {e}")
        return
    encoder.to(device)
    # Override the SD model's cond_stage_model if possible
    cond = getattr(sd_model, "cond_stage_model", None)
    if cond is None:
        print("[T5XXL] No cond_stage_model found in SD model; cannot apply T5 encoder.")
        return
    # Replace tokenizer and transformer (clip) with T5's
    cond.tokenizer = tokenizer
    # Some SD versions use .transformer, others .text_model; set both if they exist
    if hasattr(cond, "transformer"):
        cond.transformer = encoder
    if hasattr(cond, "text_model"):
        cond.text_model = encoder
    cond.dtype = torch.float32
    print("[T5XXL] Replacement complete. Using T5XXL-Unchained for text encoding.")

# Register the callback
script_callbacks.on_model_loaded(replace_with_t5)
