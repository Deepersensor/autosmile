# AutoSmile 😄

**AutoSmile** is a powerful and lightweight CLI tool and library that brings smiles to faces in your images! Whether you want to add a smile to a neutral face or enhance an existing one, AutoSmile gives you express control over every parameter. Transform your photos and spread happiness with ease! 🎉

## Features 🚀

- **Easy to Use**: Simple command-line interface for quick processing.
- **Highly Configurable**: Adjust processing, input, and output parameters via `config.json` or CLI arguments.
- **Batch Processing**: Handle single images or multiple images seamlessly.
- **Lightweight**: Minimal dependencies ensure smooth performance.

## Installation 📦

Install AutoSmile using pip:

```bash
pip install autosmile
```

Or clone the repository and install the requirements:

```bash
git clone https://github.com/yourusername/autosmile.git
cd autosmile
pip install -r requirements.txt
```

## Usage 🛠️

### Command Line Interface

Add or enhance smiles in your images with the CLI:

```bash
autosmile --input path/to/image.jpg --output path/to/output/
```

Adjust the smile intensity (from 0.0 to 1.0):

```bash
autosmile --input path/to/image.jpg --output path/to/output/ --smile_intensity 0.8
```

Process all images in a directory:

```bash
autosmile --input path/to/input_folder/ --output path/to/output_folder/
```

### Configuration File

Customize settings using `config.json`:

```json
{
    "smile_intensity": 0.5,
    "input_folder": "input_images",
    "output_folder": "output_images"
}
```

## Examples 🌟

Before                                             |  After
:-------------------------------------------------:|:-------------------------------------------------:
![Before](docs/images/before.jpg)                  |  ![After](docs/images/after.jpg)

## Contributing 🤝

Contributions are welcome! Please open an issue or submit a pull request.

## License 📄

This project is licensed under the MIT License.

## Contact 📧

Have questions or suggestions? Reach out at [your.email@example.com](mailto:your.email@example.com).
