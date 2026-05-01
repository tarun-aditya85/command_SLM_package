#!/usr/bin/env python3
"""
Inference engine for command_SLM.
Generate shell commands from natural language prompts.
"""

from typing import Optional
from llama_cpp import Llama
from .prompt_templates import format_prompt, validate_instruction, suggest_better_prompt

class InsufficientPromptError(Exception):
    """Raised when user prompt is too vague or unclear"""
    pass

def generate_command(
    llm: Llama,
    user_prompt: str,
    max_tokens: int = 256,
    temperature: float = 0.1,
    include_context: bool = True
) -> str:
    """
    Generate shell command from natural language prompt.

    Args:
        llm: Loaded Llama model instance
        user_prompt: Natural language instruction
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature (0.1 for deterministic)
        include_context: Whether to include system context in prompt

    Returns:
        Generated shell command string

    Raises:
        InsufficientPromptError: If prompt is too vague
    """
    # Validate instruction
    is_valid, error_msg = validate_instruction(user_prompt)

    if not is_valid:
        suggestion = suggest_better_prompt(user_prompt)
        raise InsufficientPromptError(
            f"{error_msg}\n\n{suggestion}\n\n"
            f"Example: 'find all PDF files in downloads folder'"
        )

    # Format prompt
    formatted_prompt = format_prompt(user_prompt, include_context=include_context)

    # Generate with constraints
    try:
        output = llm(
            formatted_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=["\n", "###", "Instruction:"],  # Stop tokens
            echo=False
        )

        # Extract generated text
        command = output['choices'][0]['text'].strip()

        # Post-process command
        command = clean_generated_command(command)

        # Validate generated command
        if not command or len(command) < 2:
            raise InsufficientPromptError(
                "Could not generate a valid command from your prompt.\n"
                f"{suggest_better_prompt(user_prompt)}"
            )

        return command

    except KeyError as e:
        raise RuntimeError(f"Unexpected model output format: {e}")
    except Exception as e:
        if isinstance(e, InsufficientPromptError):
            raise
        raise RuntimeError(f"Generation failed: {e}")

def clean_generated_command(command: str) -> str:
    """
    Clean up generated command text.

    Args:
        command: Raw generated command

    Returns:
        Cleaned command string
    """
    # Remove common artifacts
    if command.startswith("Command:"):
        command = command[8:].strip()

    # Remove leading/trailing whitespace
    command = command.strip()

    # Remove quotes if command is wrapped in them
    if command.startswith('"') and command.endswith('"'):
        command = command[1:-1]
    elif command.startswith("'") and command.endswith("'"):
        command = command[1:-1]

    # Remove trailing punctuation
    while command and command[-1] in '.!?':
        command = command[:-1]

    return command.strip()

def batch_generate_commands(
    llm: Llama,
    prompts: list[str],
    **kwargs
) -> list[tuple[str, Optional[str], Optional[str]]]:
    """
    Generate commands for multiple prompts.

    Args:
        llm: Loaded Llama model
        prompts: List of natural language instructions
        **kwargs: Additional arguments for generate_command

    Returns:
        List of (prompt, command, error) tuples
    """
    results = []

    for prompt in prompts:
        try:
            command = generate_command(llm, prompt, **kwargs)
            results.append((prompt, command, None))
        except Exception as e:
            results.append((prompt, None, str(e)))

    return results

if __name__ == "__main__":
    # Test inference
    print("Testing inference engine...")
    print("=" * 60)

    # Test prompts
    test_prompts = [
        "List all files larger than 100MB",
        "",  # Should fail
        "hi",  # Should fail
        "Find Python files in current directory",
        "Show disk usage",
    ]

    print("Note: This requires a loaded model. Simulating validation only.\n")

    for prompt in test_prompts:
        print(f"Prompt: '{prompt}'")

        try:
            is_valid, error = validate_instruction(prompt)
            if not is_valid:
                print(f"  ✗ Validation failed: {error}")
            else:
                print(f"  ✓ Valid prompt")
                formatted = format_prompt(prompt)
                print(f"  Formatted: {formatted[:50]}...")
        except Exception as e:
            print(f"  ✗ Error: {e}")

        print()
