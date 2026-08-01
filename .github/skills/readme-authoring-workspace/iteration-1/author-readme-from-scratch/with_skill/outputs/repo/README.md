# tinytoml

A tiny, dependency-free TOML parser and serializer for Python. Read a TOML string into a plain
`dict`, and write a `dict` back out as TOML.

## Why tinytoml

- **Small and dependency-free** — a single module you can vendor if you like.
- **Round-trips** — `parse` and `dumps` are inverses for the common TOML subset.
- **Plain data** — you get ordinary Python `dict`s, not custom objects.

## Installation

```
pip install tinytoml
```

## Usage

```python
import tinytoml

data = tinytoml.parse(
    """
    title = "example"

    [owner]
    name = "Ada"
    """
)
print(data["owner"]["name"])  # -> Ada

print(tinytoml.dumps({"title": "example", "owner": {"name": "Ada"}}))
```

## Getting help

Have a question or hit a bug? Open an issue in the [issue tracker](../../issues) and include a small
TOML snippet that reproduces it.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

Released under the MIT License — see [LICENSE](LICENSE).
