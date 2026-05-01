#!/usr/bin/env python3
"""
Prompt templates for command_SLM.
Format user instructions into model-ready prompts.
"""

import os
import platform
from typing import Dict, Optional

def get_system_context() -> Dict[str, str]:
    """
    Get current system context for command generation.

    Returns:
        Dict with 'cwd', 'os', and 'shell' information
    """
    return {
        'cwd': os.getcwd(),
        'os': platform.system().lower(),
        'shell': os.environ.get('SHELL', 'bash').split('/')[-1]
    }

def format_prompt(
    user_instruction: str,
    include_context: bool = True,
    context: Optional[Dict[str, str]] = None
) -> str:
    """
    Format user instruction into model prompt.

    The model was trained on this format:
    Instruction: <instruction>
    [Input: <context>]
    Command: <command>

    Args:
        user_instruction: Natural language command request
        include_context: Whether to include system context
        context: Optional custom context dict

    Returns:
        Formatted prompt string
    """
    # Start with instruction
    prompt = f"Instruction: {user_instruction}\n"

    # Add context if requested
    if include_context:
        if context is None:
            context = get_system_context()

        # Only add context if it's informative
        if context:
            context_parts = []

            if 'os' in context and context['os']:
                context_parts.append(f"OS: {context['os']}")

            if 'cwd' in context and context['cwd']:
                # Simplify long paths
                cwd = context['cwd']
                if len(cwd) > 50:
                    cwd = "..." + cwd[-47:]
                context_parts.append(f"Directory: {cwd}")

            if context_parts:
                prompt += f"Input: {', '.join(context_parts)}\n"

    # Add command prefix for generation
    prompt += "Command:"

    return prompt

def format_examples() -> str:
    """
    Get example prompts for demonstration.

    Returns:
        String with example prompts and expected outputs
    """
    examples = [
        ("List all files larger than 100MB", "find . -size +100M -type f -ls"),
        ("Find processes using more than 50% CPU", "ps aux | awk '$3 > 50 {print $0}'"),
        ("Compress logs directory with timestamp", "tar -czf logs_$(date +%Y%m%d_%H%M%S).tar.gz logs/"),
        ("Search for 'error' in all log files", "grep -r 'error' *.log"),
        ("Show disk usage sorted by size", "du -sh * | sort -hr"),
    ]

    output = "Example Prompts:\n"
    output += "=" * 60 + "\n"

    for instruction, command in examples:
        output += f"\nInstruction: {instruction}\n"
        output += f"Command: {command}\n"

    return output

def validate_instruction(instruction: str) -> tuple[bool, Optional[str]]:
    """
    Validate user instruction for common issues.

    Args:
        instruction: User's natural language instruction

    Returns:
        (is_valid, error_message) tuple
    """
    # Check if empty
    if not instruction or not instruction.strip():
        return False, "Instruction cannot be empty"

    # Check if too short
    if len(instruction.strip()) < 5:
        return False, "Instruction is too vague. Please be more specific."

    # Check if it's already a command (basic heuristic)
    common_commands = ['ls', 'cd', 'pwd', 'cat', 'grep', 'find', 'tar', 'chmod']
    first_word = instruction.strip().split()[0].lower()

    if first_word in common_commands and ' ' in instruction and instruction.count(' ') < 3:
        return False, "This looks like a shell command already. Try describing what you want to do."

    return True, None

def suggest_better_prompt(instruction: str) -> str:
    """
    Suggest improvements for vague prompts.

    Args:
        instruction: Original instruction

    Returns:
        Suggestion string
    """
    suggestions = []

    # Check for common vague terms
    vague_terms = {
        'files': 'What type of files? (e.g., "all PDF files", "Python files larger than 1MB")',
        'delete': 'Be specific: what should be deleted and under what conditions?',
        'show': 'What should be shown? (e.g., "show disk usage", "show running processes")',
        'find': 'What should be found? Where? (e.g., "find Python files in src directory")',
    }

    instruction_lower = instruction.lower()

    for term, suggestion in vague_terms.items():
        if term in instruction_lower:
            suggestions.append(suggestion)

    if suggestions:
        return "Try being more specific:\n  - " + "\n  - ".join(suggestions)
    else:
        return "Try adding more details about what you want to do."

if __name__ == "__main__":
    # Test prompt formatting
    print("Testing prompt templates...")
    print("=" * 60)

    # Test basic formatting
    instruction = "List all files larger than 100MB"
    prompt = format_prompt(instruction)
    print("Basic Prompt:")
    print(prompt)
    print()

    # Test with custom context
    custom_context = {
        'os': 'darwin',
        'cwd': '/Users/test/projects',
        'shell': 'zsh'
    }
    prompt_with_context = format_prompt(instruction, context=custom_context)
    print("Prompt with Context:")
    print(prompt_with_context)
    print()

    # Test validation
    print("Validation Tests:")
    test_cases = [
        "",
        "hi",
        "ls -la",
        "List all files larger than 100MB"
    ]

    for test in test_cases:
        is_valid, error = validate_instruction(test)
        print(f"  '{test}' -> Valid: {is_valid}, Error: {error}")

    print("\n" + "=" * 60)
    print("Examples:")
    print(format_examples())
