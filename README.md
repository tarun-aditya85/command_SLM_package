# command-slm

**AI-powered CLI for natural language to shell commands**

Turn natural language instructions into executable shell commands using a local small language model (SLM).

## Features

- 🤖 **Local AI Model**: Runs entirely on your machine (no cloud API needed)
- 🔒 **Privacy-First**: All processing happens locally
- ⚡ **Fast**: Generates commands in <2 seconds on CPU
- 🎯 **Accurate**: Fine-tuned on 10K+ bash command examples
- 🛡️ **Safe**: Double-confirmation workflow prevents accidental execution
- 🌐 **Cross-Platform**: Works on Mac, Ubuntu, and Linux

## Installation

```bash
pip install command-slm
```

On first use, the CLI will automatically download the model (~500MB) from Hugging Face and cache it locally.

## Quick Start

```bash
# Generate and execute commands from natural language
command-slm "list all files larger than 100MB"
command-slm "find and delete .log files older than 30 days"
command-slm "compress src directory with timestamp"
```

## Usage

### Basic Syntax

```bash
command-slm "<natural language instruction>"
```

### Example Commands

```bash
# File operations
command-slm "copy all PDFs from downloads to backup"
command-slm "find duplicate files in current directory"
command-slm "count lines of code in Python files"

# System monitoring
command-slm "show disk usage sorted by size"
command-slm "find processes using more than 50% CPU"
command-slm "monitor network connections on port 8080"

# Text processing
command-slm "search for 'error' in all log files"
command-slm "replace old_name with new_name in all files"
command-slm "count unique IP addresses in access.log"
```

### Workflow

1. **Enter instruction**: Natural language description of what you want
2. **Review command**: See generated command with syntax highlighting
3. **Confirm**: Press ENTER to review, ENTER again to execute
4. **Cancel**: Press ESC at any point to abort

### Command-Line Options

```bash
command-slm --help          # Show help message
command-slm --version       # Show version
command-slm --clear-cache   # Clear downloaded model
command-slm --no-context    # Don't include system context
command-slm --verbose       # Enable detailed output
```

## How It Works

1. **Model Download**: First-time use downloads a 500MB quantized model from Hugging Face
2. **Local Inference**: Command generation runs entirely on your CPU/GPU
3. **Prompt Engineering**: Your instruction is formatted with system context
4. **Generation**: Model generates shell command (typically <2s on modern CPUs)
5. **Validation**: Command is validated for basic safety
6. **Confirmation**: Double-ENTER workflow prevents accidental execution

## Requirements

- **Python**: 3.8 or higher
- **RAM**: 8GB recommended for smooth performance
- **Disk**: ~1GB for model cache
- **OS**: Mac, Ubuntu, Debian, or other Linux distributions

## Tips for Better Results

✅ **Be specific**:
- "list all PDF files" → Better than "show files"
- "files larger than 100MB" → Better than "big files"

✅ **Include context**:
- "in downloads folder" → Specifies location
- "modified in last 7 days" → Specifies time range

✅ **State the goal**:
- "find and delete old logs" → Clear intent
- "compress with timestamp" → Specific requirement

❌ **Avoid vague prompts**:
- "do something" → Too vague
- "fix it" → Unclear what needs fixing

## Safety Features

- **Preview Before Execution**: Always shows command before running
- **Double Confirmation**: Requires two ENTER presses to execute
- **ESC to Cancel**: Quick escape at any confirmation point
- **Command Validation**: Basic checks for empty or malformed commands

**⚠️ Warning**: Always review generated commands carefully. While the model is trained on safe examples, it can still generate incorrect or potentially destructive commands. The responsibility for execution lies with you.

## Model Details

- **Architecture**: Phi-2 (2.7B parameters) with QLoRA
- **Format**: 4-bit GGUF quantized
- **Training Data**: 10K bash command-instruction pairs
- **Inference**: llama.cpp backend for efficient CPU inference
- **Size**: ~500MB on disk
- **License**: MIT

## Development

### Installation from Source

```bash
git clone https://github.com/lmv/command-slm.git
cd command-slm
pip install -e .
```

### Running Tests

```bash
pip install pytest pytest-cov
pytest tests/
```

### Building Package

```bash
python -m build
pip install dist/command_slm-*.whl
```

## Troubleshooting

### Model Download Fails

```bash
# Clear cache and retry
command-slm --clear-cache
command-slm "list files"
```

### Slow Inference

- Ensure you have 8GB+ RAM available
- Close other memory-intensive applications
- Consider using a machine with GPU support

### Command Not Found After Install

```bash
# Ensure pip bin directory is in PATH
pip show command-slm  # Check installation location
which command-slm     # Verify it's in PATH
```

## Related Projects

- **Model Training**: [command_SLM](https://github.com/lmv/command_SLM) - Training code and datasets
- **Model on HuggingFace**: [lmv/command-slm](https://huggingface.co/lmv/command-slm)

## Contributing

Contributions welcome! Areas of interest:
- Additional command patterns and examples
- Cross-platform compatibility improvements
- Performance optimizations
- Better error handling and validation

## License

MIT License - see LICENSE file for details

## Author

**Lalitha M V**

Senior Manager, Software Engineering @ Salesforce

## Acknowledgments

- Built on [Microsoft Phi-2](https://huggingface.co/microsoft/phi-2)
- Uses [llama.cpp](https://github.com/ggerganov/llama.cpp) for efficient inference
- Trained on open-source bash command datasets from Hugging Face
# command_SLM_package
