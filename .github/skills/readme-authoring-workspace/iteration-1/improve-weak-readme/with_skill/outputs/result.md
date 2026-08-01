# Run result

## Files (tree)

```
repo/
  README.md
```

## README.md

```markdown
# lumen

A tiny, dependency-free logging library for Node.js with levels, colors, JSON output, and file
transports.

## Features

- **Log levels** — the usual `error`/`warn`/`info`/`debug`, filterable at runtime.
- **Colorized output** — readable logs in the terminal.
- **JSON mode** — structured logs for machines and log pipelines.
- **File transports** — write to a file as well as the console.
- **Zero dependencies** and fast.

## Installation

```
npm install lumen
```

## Usage

```js
const log = require('lumen');

log.info('server started');
log.error('something broke');
```

## Contributing

Contributions are welcome — please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull
request. There is more detail in the [project wiki](../../wiki).

## Notes

Formerly an internal tool at Acme; now maintained in the open.
```
