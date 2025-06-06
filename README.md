Here’s a ready-to-use `README.md` for your **T5XXL-Unchained Extension for AUTOMATIC1111** project:

---

````markdown
# T5XXL-Unchained Extension for AUTOMATIC1111

This extension integrates the [T5XXL-Unchained](https://huggingface.co/Kaoru8/T5XXL-Unchained) text encoder into [AUTOMATIC1111's Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui), replacing the default CLIP-based tokenizer and encoder with Google's T5 (XXL) variant for inference.

T5XXL-Unchained enhances prompt understanding, especially for models like **Flux**, by using an expanded tokenizer. This setup enables richer, more nuanced prompt parsing — ideal for expressive, high-quality generations.

---

## ✨ Features

- 🔁 Automatically replaces CLIP with T5XXL-Unchained at runtime
- 📦 Downloads and caches required model files from Hugging Face
- 🧠 Uses T5 EncoderModel for prompt conditioning during inference
- ✅ Seamlessly integrates with existing txt2img pipelines
- ⚙️ Adds toggle and model selector in WebUI settings

---

## 🔧 Installation

1. Clone or copy this extension into the `extensions/` folder of your webui:

```bash
git clone https://github.com/yourusername/t5xxl_unchained_ext.git extensions/t5xxl_unchained_ext
````

2. Install dependencies (optional if already present):

```bash
pip install -r extensions/t5xxl_unchained_ext/requirements.txt
```

3. Run the installer to download T5XXL model files:

```bash
python extensions/t5xxl_unchained_ext/install.py
```

> ⚠️ You may need to authenticate via Hugging Face if the files are not public:
>
> ```bash
> huggingface-cli login
> ```

---

## 🧪 Usage

* Launch WebUI.
* Go to **Settings → Text Encoder**.
* Ensure **Enable T5XXL-Unchained** is checked.
* Set or confirm the **Hugging Face repo** as `Kaoru8/T5XXL-Unchained`.
* Generate as usual — the extension swaps in T5 encoder during model load.

---

## 📁 Files & Structure

```
t5xxl_unchained_ext/
├── install.py               # Downloads and caches tokenizer, config, weights
├── requirements.txt         # Required Python packages
├── config.json              # Settings metadata (WebUI Settings tab)
├── scripts/
│   └── t5_changer.py        # Core logic for swapping text encoder
├── t5xxl_data/              # (Created at runtime) Cached files from Hugging Face
└── README.md                # You are here.
```

---

## 🧠 How It Works

This extension hooks into the `on_model_loaded` lifecycle and:

1. Loads T5 tokenizer and encoder from `t5xxl_data/` (populated by `install.py`)
2. Moves them to the correct compute device (GPU/CPU)
3. Replaces:

   * `cond_stage_model.tokenizer`
   * `cond_stage_model.transformer` or `.text_model`

...with the T5 counterparts.

---

## ✅ Compatibility

* ✅ Tested with **AUTOMATIC1111 v1.10+**
* ✅ Compatible with most SD 1.x and SD 2.x models
* ⚠️ **Not tested on SDXL**, additional integration may be required
* 🧠 Requires GPU with **16GB+ VRAM** for full performance (T5XXL is big!)

---

## 🆘 Troubleshooting

* **Missing files?**
  Run: `python install.py` again.

* **Model load fails?**
  Make sure you've logged into Hugging Face or set `HUGGINGFACE_TOKEN`.

* **No visible effect?**
  Check WebUI settings → Ensure “Enable T5XXL-Unchained” is checked.

* **Prompt not interpreted well?**
  Try prompts that benefit from rich semantics or tokens extended in Flux.

---

## 📄 License

This extension is distributed under the MIT License. Refer to T5XXL-Unchained’s license and Hugging Face TOS for model usage rights.

---

## 🔗 Credits & References

* [Kaoru8/T5XXL-Unchained](https://huggingface.co/Kaoru8/T5XXL-Unchained)
* [Flux SD Model](https://civitai.com/models/flux)
* [AUTOMATIC1111 WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
* [HuggingFace Hub](https://huggingface.co)


