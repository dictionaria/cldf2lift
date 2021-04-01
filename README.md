# CLDF to LIFT conversion

Converts a CLDF Dictionary

# Installation

## Stand-alone command-line interface

    pip install -e .

## With CLDFbench integration

    pip install -e .[cldfbench]

# Usage

## Stand-alone command-line interface

```
usage: cldf2lift [-h] [-o FILENAME] [-l LANG] [--meta-language LANG]
                 [--meta-language-2 LANG] [--meta-language-3 LANG]
                 CLDF-METADATA

Convert a dictionary from the Cross Linguistic Data Formats (CLDF) to the
Lexicon Interchange FormaT (LIFT). This program expects the following
convention regarding the meta languages: The *primary meta language* refers to
the language used in the `Description` column of the `SenseTable`. The
*secondary meta language* refers to the language used in the
`alt_translation1` column of the `SenseTable`. The *tertiary meta language*
refers to the language used in the `alt_translation2` column of the
`SenseTable`. Note: For all language codes, LIFT expects two-letter ISO 639-1
codes (e.g. `en` for English). If such a code is not available for your
language, fall back to its three-letter ISO 639-2/3 code.

positional arguments:
  CLDF-METADATA         CLDF metadata file

optional arguments:
  -h, --help            show this help message and exit
  -o FILENAME, --output FILENAME
                        Output file or `-` for standard output [default: -]
  -l LANG, --language LANG
                        ISO 639-1 code of the language [default: und]
  --meta-language LANG  ISO 639-1 code of the primary meta language [default:
                        en]
  --meta-language-2 LANG
                        ISO 639-1 code of the secondary meta language
                        [default: None]
  --meta-language-3 LANG
                        ISO 639-1 code of the tertiary meta language [default:
                        None]
```

## CLDFbench subcommand

```
usage: cldfbench lift.lift [-h] [--entry-point ENTRY_POINT] [-o FILENAME]
                           [-l LANG] [--meta-language LANG]
                           [--meta-language-2 LANG] [--meta-language-3 LANG]
                           DATASET

Convert CLDF dataset into the Lexicon Interchange FormaT (LIFT).

positional arguments:
  DATASET               Dataset spec, either ID of installed dataset or path
                        to python module.

optional arguments:
  -h, --help            show this help message and exit
  --entry-point ENTRY_POINT
                        Name of entry_points to identify datasets (default:
                        cldfbench.dataset)
  -o FILENAME, --output FILENAME
                        Output file [default: ./<sid>.lift] (default: None)
  -l LANG, --language LANG
                        ISO 639-1 code of the language [default: und]
                        (default: und)
  --meta-language LANG  ISO 639-1 code of the primary meta language [default:
                        en] (default: en)
  --meta-language-2 LANG
                        ISO 639-1 code of the secondary meta language
                        [default: None] (default: None)
  --meta-language-3 LANG
                        ISO 639-1 code of the tertiary meta language [default:
                        None] (default: None)
```
