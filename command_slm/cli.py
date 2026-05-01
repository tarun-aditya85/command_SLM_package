#!/usr/bin/env python3
"""
Main CLI entry point for command-slm.
"""

import sys
import subprocess
import argparse
from typing import NoReturn

from .model_manager import load_model, clear_cache
from .inference import generate_command, InsufficientPromptError
from .ui import (
    preview_command,
    show_error,
    show_success,
    show_help,
    show_version,
    console
)

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        prog="command-slm",
        description="AI-powered CLI for natural language to shell commands",
        add_help=False
    )

    parser.add_argument(
        "instruction",
        nargs="*",
        help="Natural language instruction"
    )

    parser.add_argument(
        "--help", "-h",
        action="store_true",
        help="Show help message"
    )

    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="Show version information"
    )

    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear model cache"
    )

    parser.add_argument(
        "--no-context",
        action="store_true",
        help="Don't include system context in prompt"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    return parser.parse_args()

def execute_command(command: str) -> int:
    """
    Execute shell command.

    Args:
        command: Shell command to execute

    Returns:
        Command exit code
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=False,
            text=True
        )
        return result.returncode

    except KeyboardInterrupt:
        console.print("\n[yellow]✗ Interrupted[/yellow]")
        return 130

    except Exception as e:
        show_error(f"Command execution failed: {e}")
        return 1

def handle_clear_cache() -> NoReturn:
    """Handle --clear-cache flag"""
    console.print("Clearing model cache...")
    clear_cache()
    sys.exit(0)

def main() -> NoReturn:
    """Main CLI entry point"""
    # Parse arguments
    args = parse_args()

    # Handle flags
    if args.help:
        show_help()
        sys.exit(0)

    if args.version:
        show_version()
        sys.exit(0)

    if args.clear_cache:
        handle_clear_cache()

    # Get instruction
    if not args.instruction:
        show_error("No instruction provided")
        console.print("Usage: command-slm \"<instruction>\"")
        console.print("Try: command-slm --help")
        sys.exit(1)

    user_prompt = " ".join(args.instruction)

    try:
        # Load model
        console.print("[dim]Loading command_SLM model...[/dim]")

        llm = load_model(verbose=args.verbose)

        # Generate command
        console.print(f"\n[dim]Processing:[/dim] {user_prompt}")

        command = generate_command(
            llm,
            user_prompt,
            include_context=not args.no_context
        )

        # Preview and confirm
        confirmed = preview_command(command)

        if not confirmed:
            console.print("[yellow]Command cancelled by user[/yellow]")
            sys.exit(0)

        # Execute command
        exit_code = execute_command(command)

        # Show result
        if exit_code == 0:
            show_success("Command completed successfully")
        else:
            show_error(f"Command exited with code {exit_code}")

        sys.exit(exit_code)

    except InsufficientPromptError as e:
        show_error(str(e))
        sys.exit(1)

    except KeyboardInterrupt:
        console.print("\n[yellow]✗ Interrupted[/yellow]")
        sys.exit(130)

    except Exception as e:
        show_error(f"Unexpected error: {e}")

        if args.verbose:
            import traceback
            console.print("\n[dim]Traceback:[/dim]")
            traceback.print_exc()

        sys.exit(1)

if __name__ == "__main__":
    main()
