#!/usr/bin/env python3
"""
Terminal UI for command_SLM.
Display command preview and handle user confirmation.
"""

import sys
import tty
import termios
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text

console = Console()

def preview_command(command: str) -> bool:
    """
    Display command preview and get user confirmation.

    Flow:
    1. Show generated command with syntax highlighting
    2. Wait for first ENTER (preview)
    3. Wait for second ENTER (execute) or ESC (cancel)

    Args:
        command: Generated shell command

    Returns:
        True if user confirms execution, False if cancelled
    """
    # Display command with syntax highlighting
    syntax = Syntax(command, "bash", theme="monokai", line_numbers=False)
    panel = Panel(
        syntax,
        title="[bold blue]Generated Command[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    )

    console.print()
    console.print(panel)
    console.print()

    # First confirmation prompt
    console.print(
        "[yellow]Press ENTER to review[/yellow] | "
        "[dim]ESC to cancel[/dim]"
    )

    first_key = wait_for_keypress()

    if first_key == 'esc':
        console.print("[red]✗ Cancelled[/red]")
        return False

    # Second confirmation prompt
    console.print()
    console.print(
        "[green bold]Press ENTER again to execute[/green bold] | "
        "[dim]ESC to cancel[/dim]"
    )

    second_key = wait_for_keypress()

    if second_key == 'esc':
        console.print("[red]✗ Cancelled[/red]")
        return False

    console.print("[green]✓ Executing...[/green]")
    console.print()
    return True

def wait_for_keypress() -> str:
    """
    Wait for Enter or Escape keypress.

    Returns:
        'enter' or 'esc'
    """
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)

        # Handle Enter key
        if ch == '\r' or ch == '\n':
            return 'enter'

        # Handle Escape key
        elif ch == '\x1b':
            return 'esc'

        # Handle Ctrl+C
        elif ch == '\x03':
            raise KeyboardInterrupt

        # Any other key, treat as cancel
        else:
            return 'esc'

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def show_error(error_message: str):
    """Display error message"""
    console.print()
    console.print(f"[red bold]✗ Error:[/red bold] {error_message}")
    console.print()

def show_success(message: str):
    """Display success message"""
    console.print()
    console.print(f"[green]✓ {message}[/green]")
    console.print()

def show_help():
    """Display help information"""
    help_text = """
[bold cyan]command-slm[/bold cyan] - AI-powered CLI for natural language to shell commands

[bold]USAGE:[/bold]
    command-slm "<natural language instruction>"

[bold]EXAMPLES:[/bold]
    command-slm "list all files larger than 100MB"
    command-slm "find and delete old log files"
    command-slm "compress directory with timestamp"
    command-slm "show disk usage sorted by size"

[bold]WORKFLOW:[/bold]
    1. Enter natural language instruction
    2. Review generated command (syntax highlighted)
    3. Press ENTER to confirm
    4. Press ENTER again to execute
    5. Press ESC at any point to cancel

[bold]TIPS:[/bold]
    • Be specific with your instructions
    • Include file types, sizes, time ranges when relevant
    • Review the command carefully before executing
    • Use ESC to cancel at any confirmation step

[bold]OPTIONS:[/bold]
    --help, -h          Show this help message
    --version, -v       Show version information
    --clear-cache       Clear downloaded model cache

[bold]SAFETY:[/bold]
    Always review generated commands before execution.
    The double-confirmation workflow prevents accidental execution.

For more information, visit: https://github.com/lmv/command-slm
"""
    console.print(help_text)

def show_version():
    """Display version information"""
    from . import __version__
    console.print(f"command-slm version {__version__}")

if __name__ == "__main__":
    # Test UI components
    print("Testing UI components...")
    print()

    # Test command preview
    test_command = "find . -name '*.py' -type f -exec wc -l {} +"

    print("Test: Command Preview")
    print("-" * 60)

    confirmed = preview_command(test_command)

    if confirmed:
        show_success("Command execution confirmed")
    else:
        show_error("Command execution cancelled")

    print("\nTest: Help Display")
    print("-" * 60)
    show_help()
