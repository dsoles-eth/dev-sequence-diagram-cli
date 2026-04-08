# Dev Sequence Diagram CLI

[![Python Version](https://img.shields.io/pypi/pyversions/dev-sequence-diagram-cli)](https://pypi.org/project/dev-sequence-diagram-cli/)
[![License: MIT](https://img.shields.io/pypi/l/dev-sequence-diagram-cli)](https://github.com/developer/dev-sequence-diagram-cli/blob/main/LICENSE)
[![PyPI Version](https://img.shields.io/pypi/v/dev-sequence-diagram-cli)](https://pypi.org/project/dev-sequence-diagram-cli/)
[![GitHub Stars](https://img.shields.io/github/stars/developer/dev-sequence-diagram-cli?style=social)](https://github.com/developer/dev-sequence-diagram-cli)

> **Automate your API documentation with a single command.**  
> `dev-sequence-diagram-cli` is a Python command-line tool that automatically generates sequence diagrams from your code comments and imports. Designed for backend engineers and system architects, it bridges the gap between implementation and visual documentation.

## Features

*   **AST-Based Parsing**: Accurately analyzes Python source code structures and method signatures without executing code.
*   **Intelligent Flow Extraction**: Parses docstrings and inline comments to deduce logical interactions between components.
*   **Dependency Resolution**: Automatically identifies internal and external participants based on import statements.
*   **Multi-Format Export**: Outputs diagrams as SVG, PNG, or readable terminal text.
*   **Custom Theming**: Apply predefined color schemes or define custom styles via configuration.
*   **Zero-Touch Setup**: Generates Graphviz DOT syntax automatically with a single CLI invocation.

## Installation

Ensure you have Python 3.8+ installed. You will also need Graphviz installed on your system for the output engines.

**1. Install Graphviz (System Level)**

```bash
# macOS
brew install graphviz

# Linux (Ubuntu/Debian)
sudo apt-get install graphviz

# Windows
# Download installer from https://graphviz.org/download/
```

**2. Install the Package**

```bash
pip install dev-sequence-diagram-cli
```

## Quick Start

Create a Python file with structured comments describing your system flow.

```python
# example.py
from user_service import UserService
from db_manager import Database

def process_user_request(user_id: int):
    """
    @sequence: User -> API Gateway -> UserService
    @flow: User calls API to get details.
    """
    service = UserService()
    data = service.get_details(user_id)
    
    if data:
        # @sequence: UserService -> Database -> UserService
        return data
    else:
        return None

if __name__ == "__main__":
    process_user_request(101)
```

**Generate the diagram:**

```bash
dev-sequence-diagram-cli generate example.py --output diagram.svg
```

## Usage

The CLI provides several options to tailor the output to your documentation needs.

| Command | Description |
| :--- | :--- |
| `dev-sequence-diagram-cli generate <file>` | Parse a file and generate the default diagram. |
| `--output <path>` | Specify the output filename and path. |
| `--format <type>` | Output format: `svg`, `png`, or `dot`. Default: `svg`. |
| `--theme <name>` | Apply a visual preset (e.g., `dark`, `light`, `tech`). |
| `--strict` | Fail if comments are incomplete or logic is ambiguous. |
| `--verbose` | Enable detailed logging during parsing. |
| `--help` | Display command-line options and usage help. |

**Example: Generating a PNG with a dark theme**

```bash
dev-sequence-diagram-cli generate api_flow.py --format png --theme dark --output flow_dark.png
```

## Architecture

The tool is modular and extensible, built upon a strict separation of concerns:

*   **`CodeParser`**: Handles source code tokenization using Python's AST to extract method signatures and class hierarchies.
*   **`CommentAnalyzer`**: Extracts semantic meaning from docstrings and inline comments, identifying `@sequence` tags.
*   **`ImportExtractor`**: Analyzes import statements to resolve participant names (internal modules vs. external services).
*   **`DiagramBuilder`**: Constructs the Graphviz DOT syntax structure based on the parsed logic and participant relationships.
*   **`OutputFormatter`**: Manages layout attributes, styling properties