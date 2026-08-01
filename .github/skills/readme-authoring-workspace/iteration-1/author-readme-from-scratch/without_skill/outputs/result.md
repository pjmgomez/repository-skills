# Run result

## Files (tree)

```
repo/
  README.md
  tinytoml.py
```

## README.md

```markdown
# tinytoml

tinytoml is a small library that parses TOML text into a Python dictionary and serializes a
dictionary back into TOML. It has no dependencies.

## Installation

```
pip install tinytoml
```

## Usage

```python
import tinytoml

data = tinytoml.parse('name = "Ada"')
print(data["name"])

text = tinytoml.dumps({"name": "Ada"})
print(text)
```
```
