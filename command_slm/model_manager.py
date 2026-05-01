#!/usr/bin/env python3
"""
Model manager for command_SLM.
Handles model download from Hugging Face and caching.
"""

from pathlib import Path
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

# Configuration
DEFAULT_REPO_ID = "lmv/command-slm"  # Will be updated after model upload
DEFAULT_FILENAME = "command_slm_q4.gguf"
CACHE_DIR = Path.home() / ".cache" / "command_slm"

def get_model_path() -> Path:
    """Get the local path to the cached model"""
    return CACHE_DIR / DEFAULT_FILENAME

def download_model(
    repo_id: str = DEFAULT_REPO_ID,
    filename: str = DEFAULT_FILENAME,
    force_download: bool = False
) -> Path:
    """
    Download model from Hugging Face Hub.

    Args:
        repo_id: Hugging Face repository ID
        filename: Model filename to download
        force_download: Force re-download even if cached

    Returns:
        Path to downloaded model file
    """
    model_path = get_model_path()

    # Check if model already exists
    if model_path.exists() and not force_download:
        print(f"✓ Using cached model: {model_path}")
        return model_path

    # Create cache directory
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    print(f"📦 Downloading command_SLM model from Hugging Face...")
    print(f"   Repository: {repo_id}")
    print(f"   File: {filename} (~500MB)")
    print(f"   This may take a few minutes...")

    try:
        # Download from Hugging Face
        downloaded_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            cache_dir=CACHE_DIR,
            local_dir=CACHE_DIR,
            local_dir_use_symlinks=False
        )

        print(f"✓ Model downloaded successfully!")
        print(f"   Cached at: {downloaded_path}")

        return Path(downloaded_path)

    except Exception as e:
        print(f"✗ Failed to download model: {e}")
        print(f"\nTroubleshooting:")
        print(f"1. Check your internet connection")
        print(f"2. Verify the repository exists: https://huggingface.co/{repo_id}")
        print(f"3. Try clearing cache: rm -rf {CACHE_DIR}")
        raise

def load_model(
    repo_id: str = DEFAULT_REPO_ID,
    filename: str = DEFAULT_FILENAME,
    n_ctx: int = 512,
    n_threads: int = 4,
    n_gpu_layers: int = 0,
    verbose: bool = False
) -> Llama:
    """
    Load GGUF model with llama-cpp-python.

    Args:
        repo_id: Hugging Face repository ID
        filename: Model filename
        n_ctx: Context window size
        n_threads: Number of CPU threads
        n_gpu_layers: Number of layers to offload to GPU (0 for CPU-only)
        verbose: Enable verbose logging

    Returns:
        Loaded Llama model instance
    """
    # Download model if not cached
    model_path = download_model(repo_id, filename)

    if not verbose:
        print("Loading command_SLM model...")

    try:
        # Load model with llama-cpp-python
        llm = Llama(
            model_path=str(model_path),
            n_ctx=n_ctx,
            n_threads=n_threads,
            n_gpu_layers=n_gpu_layers,
            verbose=verbose
        )

        if not verbose:
            print("✓ Model loaded successfully!")

        return llm

    except Exception as e:
        print(f"✗ Failed to load model: {e}")
        print(f"\nTroubleshooting:")
        print(f"1. Ensure llama-cpp-python is installed: pip install llama-cpp-python")
        print(f"2. Check model file integrity: {model_path}")
        print(f"3. Try re-downloading: rm {model_path}")
        raise

def clear_cache():
    """Clear the model cache"""
    import shutil

    if CACHE_DIR.exists():
        print(f"Clearing cache: {CACHE_DIR}")
        shutil.rmtree(CACHE_DIR)
        print("✓ Cache cleared")
    else:
        print("Cache directory does not exist")

if __name__ == "__main__":
    # Test model download and loading
    print("Testing model manager...")
    print("=" * 60)

    try:
        # Download
        model_path = download_model()
        print(f"\n✓ Download test passed")

        # Load
        llm = load_model(verbose=True)
        print(f"\n✓ Load test passed")

        # Test inference
        test_prompt = "Instruction: List files\nCommand:"
        output = llm(test_prompt, max_tokens=50, temperature=0.1, stop=["\n"])
        command = output['choices'][0]['text'].strip()

        print(f"\n✓ Inference test passed")
        print(f"Test prompt: {test_prompt}")
        print(f"Generated: {command}")

        print("\n" + "=" * 60)
        print("All tests passed!")

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
