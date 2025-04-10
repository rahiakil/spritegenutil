# My Python Utility

# Installable SpriteGen Utility Library

This is a Python library designed to provide utility functions for sprite generation and related tasks.

## Installation

To install the library, follow these steps:

1. Clone the repository:

    ```bash
    git clone git@github.com:rahiakil/spritegenutil.git
    cd spritegenutil
    ```

2. Install the library and its dependencies:

    ```bash
    pip install .
    ```

    Alternatively, you can install the dependencies manually:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

You can use the utility functions provided by the library in your Python projects. Here's an example:

```python
from spritegenutil import sprite_generator

# Example usage
sprite_generator.generate_sprite(input_data, output_path)
```

### Key Features

- `generate_sprite`: Generates a sprite from the given input data.
- `optimize_sprite`: Optimizes an existing sprite for better performance.
- `validate_sprite`: Validates the structure and format of a sprite.

## Running Tests

To ensure the library works as expected, run the test suite using:

```bash
pytest
```

Make sure you have `pytest` installed before running the tests.

## Contributing

We welcome contributions! If you'd like to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a clear description of your changes.

Feel free to open an issue for any bugs or feature requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.