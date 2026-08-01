# packmule

> A lightweight command-line tool for packing and hauling your files around.

`packmule` is an open-source Python CLI. This repository is scaffolded and ready
for development — replace the placeholder command logic in
[`src/packmule/cli.py`](src/packmule/cli.py) with your real features.

## Requirements

- Python 3.9 or newer

## Installation

Install from source while the project is under development:

```bash
git clone https://github.com/your-org/packmule.git
cd packmule
python -m pip install -e .
```

## Usage

```bash
packmule --help
packmule --version
```

You can also run it as a module:

```bash
python -m packmule --help
```

## Development

Set up a local environment with the development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

Run the test suite:

```bash
pytest
```

Lint the code:

```bash
ruff check .
```

## Project layout

```
packmule/
├── src/packmule/      # Application package (src layout)
├── tests/             # Test suite
├── docs/              # Documentation
└── pyproject.toml     # Packaging & tooling configuration
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before
opening an issue or pull request.

## Security

Found a vulnerability? Please follow the process in [SECURITY.md](SECURITY.md).

## License

`packmule` is released under the MIT License. See [LICENSE](LICENSE) for details.
