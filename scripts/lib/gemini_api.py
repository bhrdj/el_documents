"""
Gemini API integration utilities.

Provides wrapper functions for interacting with Google's Gemini API,
including API key management and text generation.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
import google.generativeai as genai


def load_api_key(key_path: Optional[str] = None) -> str:
    """
    Load Gemini API key from configuration file.

    Args:
        key_path: Path to API key file. If None, uses default location
                 (~/.config/google/everyday_apikey.txt)

    Returns:
        API key as string

    Raises:
        FileNotFoundError: If API key file doesn't exist
        ValueError: If API key file is empty
    """
    if key_path is None:
        key_path = os.path.expanduser("~/.config/google/everyday_apikey.txt")

    key_file = Path(key_path)

    if not key_file.exists():
        raise FileNotFoundError(
            f"API key file not found at {key_path}. "
            "Please create the file with your Gemini API key."
        )

    api_key = key_file.read_text().strip()

    if not api_key:
        raise ValueError(f"API key file at {key_path} is empty.")

    return api_key


def configure_gemini(api_key: Optional[str] = None, key_path: Optional[str] = None) -> None:
    """
    Configure the Gemini API with authentication.

    Args:
        api_key: API key string. If None, will load from key_path
        key_path: Path to API key file. Only used if api_key is None

    Raises:
        FileNotFoundError: If API key file doesn't exist (when loading from file)
        ValueError: If API key is empty
    """
    if api_key is None:
        api_key = load_api_key(key_path)

    genai.configure(api_key=api_key)


def call_gemini(
    prompt: str,
    model: str = "gemini-1.5-flash",
    temperature: float = 0.7,
    max_output_tokens: Optional[int] = None,
    system_instruction: Optional[str] = None,
    auto_configure: bool = True,
    **kwargs
) -> str:
    """
    Call Gemini API with a text prompt and return the response.

    Args:
        prompt: The text prompt to send to Gemini
        model: Model name (default: "gemini-1.5-flash")
               Other options: "gemini-1.5-pro", "gemini-1.0-pro"
        temperature: Sampling temperature (0.0-2.0, default: 0.7)
                    Lower = more deterministic, Higher = more creative
        max_output_tokens: Maximum tokens in response (default: None = model default)
        system_instruction: Optional system instruction for the model
        auto_configure: Automatically configure API if not already done (default: True)
        **kwargs: Additional generation config parameters

    Returns:
        Generated text response from Gemini

    Raises:
        Exception: If API call fails

    Example:
        >>> response = call_gemini("Explain what a neural network is")
        >>> print(response)
    """
    if auto_configure:
        try:
            # Try to configure if not already configured
            configure_gemini()
        except Exception:
            # If already configured, this will fail silently
            pass

    # Build generation config
    generation_config = {
        "temperature": temperature,
        **kwargs
    }

    if max_output_tokens is not None:
        generation_config["max_output_tokens"] = max_output_tokens

    # Create model
    model_kwargs = {"model_name": model}
    if system_instruction:
        model_kwargs["system_instruction"] = system_instruction

    model_instance = genai.GenerativeModel(**model_kwargs)

    # Generate response
    response = model_instance.generate_content(
        prompt,
        generation_config=generation_config
    )

    return response.text


def call_gemini_streaming(
    prompt: str,
    model: str = "gemini-1.5-flash",
    temperature: float = 0.7,
    max_output_tokens: Optional[int] = None,
    system_instruction: Optional[str] = None,
    auto_configure: bool = True,
    **kwargs
):
    """
    Call Gemini API with streaming response.

    Yields chunks of text as they're generated.

    Args:
        prompt: The text prompt to send to Gemini
        model: Model name (default: "gemini-1.5-flash")
        temperature: Sampling temperature (0.0-2.0, default: 0.7)
        max_output_tokens: Maximum tokens in response (default: None)
        system_instruction: Optional system instruction for the model
        auto_configure: Automatically configure API if not already done (default: True)
        **kwargs: Additional generation config parameters

    Yields:
        Text chunks as they're generated

    Example:
        >>> for chunk in call_gemini_streaming("Write a story"):
        ...     print(chunk, end="", flush=True)
    """
    if auto_configure:
        try:
            configure_gemini()
        except Exception:
            pass

    # Build generation config
    generation_config = {
        "temperature": temperature,
        **kwargs
    }

    if max_output_tokens is not None:
        generation_config["max_output_tokens"] = max_output_tokens

    # Create model
    model_kwargs = {"model_name": model}
    if system_instruction:
        model_kwargs["system_instruction"] = system_instruction

    model_instance = genai.GenerativeModel(**model_kwargs)

    # Generate streaming response
    response = model_instance.generate_content(
        prompt,
        generation_config=generation_config,
        stream=True
    )

    for chunk in response:
        if chunk.text:
            yield chunk.text


# Convenience function aliases
generate_text = call_gemini
generate_text_streaming = call_gemini_streaming
