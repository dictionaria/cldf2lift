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
usage: cldf2lift [-h] [-o FILENAME] [-l LANG] [--headword-column COLUMNNAME]
                 [--meta-language LANG] [--meta-language-2 LANG]
                 [--description-col-2 COLUMNNAME]
                 [--translation-col-2 COLUMNNAME] [--meta-language-3 LANG]
                 [--description-col-3 COLUMNNAME]
                 [--translation-col-3 COLUMNNAME] [--variant-col COLUMNNAME]
                 [--sense-id-col COLUMNNAME]
                 CLDF-METADATA

Convert a dictionary from the Cross Linguistic Data Formats (CLDF)
to the Lexicon Interchange FormaT (LIFT).

This program expects the following convention regarding the meta languages:

The *primary meta language* refers to the language used in the  `Description`
column of the `SenseTable`.

The *secondary meta language* refers to the language used in the
`alt_translation1` column of the `SenseTable`.

The *tertiary meta language* refers to the language used in the
`alt_translation2` column of the `SenseTable`.

Note: `alt_translation1` and `alt_translation2` are not part of the CLDF
      standard but rather a convention used by the Dictionaria project
      (dictionaria.clld.org).

positional arguments:
  CLDF-METADATA         CLDF metadata file

optional arguments:
  -h, --help            show this help message and exit
  -o FILENAME, --output FILENAME
                        Output file or `-` for standard output [default: -]
  -l LANG, --language LANG
                        ISO 639-3 code of the language [default: und]
  --headword-column COLUMNNAME
                        Column name for the headword in the desired orthography [default: Headword]
  --meta-language LANG  ISO 639-3 code of the primary meta language [default: eng]
  --meta-language-2 LANG
                        ISO 639-3 code of the secondary meta language [default: None] (Dictionaria extension)
  --description-col-2 COLUMNNAME
                        Column name for sense description in meta language 2 [default: alt_translation1]
  --translation-col-2 COLUMNNAME
                        Column name for example translation in meta language 2 [default: alt_translation1]
  --meta-language-3 LANG
                        ISO 639-3 code of the tertiary meta language [default: None] (Dictionaria extension)
  --description-col-3 COLUMNNAME
                        Column name for sense description in meta language 3 [default: alt_translation2]
  --translation-col-3 COLUMNNAME
                        Column name for example translation in meta language 3 [default: alt_translation2]
  --variant-col COLUMNNAME
                        Column name for variants [default: Variant_Form]
  --sense-id-col COLUMNNAME
                        Column name for references to sense in the example table [default: Sense_IDs]
```

## CLDFbench subcommand

```
usage: cldfbench lift.lift [-h] [--entry-point ENTRY_POINT] [-o FILENAME]
                           [-l LANG] [--headword-column COLUMNNAME]
                           [--meta-language LANG] [--meta-language-2 LANG]
                           [--description-col-2 COLUMNNAME]
                           [--translation-col-2 COLUMNNAME]
                           [--meta-language-3 LANG]
                           [--description-col-3 COLUMNNAME]
                           [--translation-col-3 COLUMNNAME]
                           [--variant-col COLUMNNAME]
                           [--sense-id-col COLUMNNAME]
                           DATASET

Convert a dictionary from the Cross Linguistic Data Formats (CLDF)
to the Lexicon Interchange FormaT (LIFT).

This program expects the following convention regarding the meta languages:

The *primary meta language* refers to the language used in the  `Description`
column of the `SenseTable`.

The *secondary meta language* refers to the language used in the
`alt_translation1` column of the `SenseTable`.

The *tertiary meta language* refers to the language used in the
`alt_translation2` column of the `SenseTable`.

Note: `alt_translation1` and `alt_translation2` are not part of the CLDF
      standard but rather a convention used by the Dictionaria project
      (dictionaria.clld.org).

positional arguments:
  DATASET               Dataset spec, either ID of installed dataset or path
                        to python module.

optional arguments:
  -h, --help            show this help message and exit
  --entry-point ENTRY_POINT
                        Name of entry_points to identify datasets (default:
                        cldfbench.dataset)
  -o FILENAME, --output FILENAME
                        Output file [default: ./<sid>.lift]
  -l LANG, --language LANG
                        ISO 639-3 code of the language [default: und]
  --headword-column COLUMNNAME
                        Column name for the headword in the desired
                        orthography [default: Headword] (default:
                        http://cldf.clld.org/v1.0/terms.rdf#headword)
  --meta-language LANG  ISO 639-3 code of the primary meta language [default:
                        eng]
  --meta-language-2 LANG
                        ISO 639-3 code of the secondary meta language
                        [default: None] (Dictionaria extension)
  --description-col-2 COLUMNNAME
                        Column name for sense description in meta language 2
                        [default: alt_translation1]
  --translation-col-2 COLUMNNAME
                        Column name for example translation in meta language 2
                        [default: alt_translation1]
  --meta-language-3 LANG
                        ISO 639-3 code of the tertiary meta language [default:
                        None] (Dictionaria extension)
  --description-col-3 COLUMNNAME
                        Column name for sense description in meta language 3
                        [default: alt_translation2]
  --translation-col-3 COLUMNNAME
                        Column name for example translation in meta language 3
                        [default: alt_translation2]
  --variant-col COLUMNNAME
                        Column name for variants [default: Variant_Form]
  --sense-id-col COLUMNNAME
                        Column name for references to sense in the example
                        table [default: Sense_IDs]
```
