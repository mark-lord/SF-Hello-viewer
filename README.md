# SF Hello

![hello thumbnail](https://raw.githubusercontent.com/g-cqd/SF-Hello/main/hello.png)

# Interactive SVG Converter for Apple Hello Lettering

This repo is a fork of https://github.com/g-cqd/SF-Hello, containing a modifier convert.py script. The one found in this repo converts JSON data of Apple's "Hello" lettering into SVG and then PNG format from the strokes found in the JSON files, allowing for an interactive, step-by-step visualization of how the graphic is constructed.

## Features

- Converts JSON stroke data to SVG format
- Generates PNG output for easy visualization (recommend using VSCode and having the .png output open)
- Interactive CLI interface for step-by-step conversion by pressing enter
- Supports multiple language versions of the "Hello" lettering

## Requirements

- Python 3.6+
- `cairosvg` library

## Installation

1. Clone this repository or download the `convert.py` script from this repo into the original repo.
2. Install the required library:

```

pip install cairosvg
```
Then use:

```

python convert.py "path/to/input.json" "path/to/output.svg"
```

For example:

```

python convert.py "JSON/hello-en.json" "./output"
```


## How it works

1. The script reads the JSON file containing the stroke data for the "Hello" lettering.
2. It counts the total number of elements (individual curve segments) in the design.
3. For each element:
   - It adds the element to the SVG
   - Saves the current state as an SVG file
   - Converts the SVG to PNG for easy viewing
4. The user can press Enter to add the next element (or 'q' to quit at any time).
5. The final SVG and PNG files are saved upon completion or quitting.

## Output

- An SVG file of the completed graphic (or the last state before quitting)
- A PNG file for easy viewing of the graphic
- CLI output showing progress and prompts

## Use Case

- Analyzing the construction of Apple's "Hello" lettering and extracting specific parts of the lettering for further use

## Notes

- This script is designed for educational and analytical purposes.
- The JSON data and resulting graphics are subject to Apple's copyright.
- This tool does not create new letterforms or allow for easy extraction of individual letters. (Sadly)

## License

Apache 2.0 I guess lol
