# epoch

Work with Unix timestamps from your terminal. Convert, format, and compare. Zero dependencies, pure Python stdlib.

## Install

```bash
pip install epoch-cli
```

Or run directly:

```bash
python epoch.py --help
```

## Usage

```bash
# Current timestamp
epoch --now

# Convert epoch to ISO
epoch 1700000000

# Convert date to epoch
epoch "2023-11-14T22:13:20Z"

# Relative time
epoch 1700000000 --format relative

# Specific timezone
epoch 1700000000 --tz +02:00

# Milliseconds
epoch --now --ms
```

## Formats

`iso`, `rfc2822`, `date`, `time`, `datetime`, `relative`

## License

MIT