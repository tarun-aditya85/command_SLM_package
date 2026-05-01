"""
command_slm: AI-powered CLI for natural language to shell commands
"""

__version__ = "0.1.0"
__author__ = "Lalitha M V"

from .model_manager import load_model, download_model
from .inference import generate_command, InsufficientPromptError
from .ui import preview_command

__all__ = [
    "load_model",
    "download_model",
    "generate_command",
    "preview_command",
    "InsufficientPromptError",
]
