# Contract extractor from PDF files

## Description:

Python script containing a set of functions to extract contract codes from PDF files.

Each contract follows a specific structure:
`XXXXXX/XXXXXX/XXX123/XXX123/XXX123`

Where:
* `XXXXXXX` corresponds to a alphabetic field.
* `XXX123` corresponds to a alphanumeric field.

This allows to create a REGEX function to extract these contracts by compiling this rule.

**TODO:**
* Add method to send info to a web server.
* Normalize (code refactoring) according to others?

## Dependencies:

To install all requirements (Python packages), using `pip`:
```bash
pip install -r requirements.txt
```

Along the process of implementing more utility functions, the requirements can be easily added in the requirements list (each package name goes in a new line).

------

The REGEX code in this folder has been based in [Uri]()'s code.

Uri's code in `bash`:

```bash
# Dependencies:
#   - `ag` (The silver searcher) https://github.com/ggreer/the_silver_searcher
#   - `pdftotext` https://poppler.freedesktop.org/

pdf_to_text() {
  local i=0
  local total=$(ls *.pdf | wc -l)

  for pdf in *.pdf; do
    i=$(($i + 1))
    pdftotext -nopgbrk -layout ${pdf}
    echo "Converted [${i}/${total}]: ${pdf}"
  done
}

extract_contracts() {
  local contract_regex='[[:alpha:]]+\/[[:alpha:]]+\/[[:alnum:]]+\/[[:alnum:]]+\/[[:alnum:]]+'

  ag -i -o ${contract_regex} *.txt > contratos
}

main() {
  pdf_to_text
  extract_contracts
}

main
```
