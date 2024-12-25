# scuid

[![PyPI](https://img.shields.io/pypi/v/scuid.svg?style=flat-square)](https://pypi.org/project/scuid/)
[![License](https://img.shields.io/pypi/l/scuid.svg?style=flat-square)](https://pypi.org/project/scuid/)
[![Downloads](https://img.shields.io/pypi/dm/scuid.svg?style=flat-square)](https://pypi.org/project/scuid/)

**scuid** is a lightweight Python library for generating collision-resistant IDs optimized for horizontal scaling and high performance. It serves as a slim, alternative implementation of [cuid] with added flexibility for customization, including support for custom random number generators.

Whether you're building distributed systems or need compact, unique identifiers, **scuid** offers a simple and efficient solution.

[cuid]: https://github.com/ericelliott/cuid

> It is a reference port of the [scuid](https://github.com/jhermsmeier/node-scuid) source code for Node.js

## Why Use scuid?

- **Compact, Unique, and Efficient**: Generates small, collision-resistant IDs suitable for distributed systems. Compared to UUID v4, MD5, SHA1, and other collision-resistant ID generators, the shorter length of scuid IDs reduces the number of characters and tokens used. This makes scuid particularly advantageous for applications like generative AI, where minimizing token usage is often crucial.
- **Customizable and Flexible**: Supports custom random number generators and configurable options, enabling tailored solutions for a wide range of use cases.
- **Lightweight and High-Performance**: Designed to deliver fast ID generation without introducing unnecessary dependencies, ensuring optimal performance.

For more information or to contribute, visit the [GitHub repository](https://github.com/lh0x00/scuid).

## Installation

Install **scuid** using [pip](https://pypi.org/project/scuid/):

```sh
pip install scuid
```

## Quick Start

### Generate a Unique ID

Create a unique identifier with just one line:

```python
from scuid import scuid

id = scuid()
print(id)
# Example output: 'ciux3hs0x0000io10cusdm8r2'
```

### Generate a Compact Slug

Slugs are shorter representations suitable for use in URLs or filenames:

```python
from scuid import slug

slug_value = slug()
print(slug_value)
# Example output: '6x1i0r0'
```

### Get the Process Fingerprint

The fingerprint represents the process and machine where the ID was generated:

```python
from scuid import fingerprint

fp = fingerprint()
print(fp)
# Example output: 'io10'
```

## Advanced Usage

### Customize the Random Number Generator (RNG)

You can provide a custom random number generator by implementing a `random()` method:

```python
from scuid import Scuid

class CustomRNG:
    def random(self):
        return 0.5  # Always returns 0.5 for demonstration purposes

custom_scuid = Scuid({"rng": CustomRNG().random})
id = custom_scuid.id()
print(id)
```

### Configure Custom Options

You can customize the ID generation process to fit your requirements. Note that altering these options may affect compatibility with the default [cuid] behavior.

```python
from scuid import Scuid

custom_scuid = Scuid({
    "prefix": "c",              # Prefix for generated IDs
    "base": 36,                 # Radix for encoding (supports 2-36)
    "blockSize": 4,             # Size of each padded block
    "fill": "0",                # Padding character
    "pid": 12345,               # Custom process ID
    "hostname": "customhost",   # Custom hostname
    "rng": lambda: 0.42,        # Custom RNG function
})

id = custom_scuid.id()
print(id)
```

## Testing

To verify the correctness and collision resistance of **scuid**, you can run the included tests:

```sh
pytest
```

The tests simulate real-world scenarios with millions of iterations to ensure the reliability of generated IDs.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
