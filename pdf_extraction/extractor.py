from glob import glob
import pdftotext
import re

# Global:
path_to_pdfs = "..."


def list_pdfs(pdf_path):
    """List all PDF files in a given path."""
    return sorted(glob(pdf_path + '/*.pdf'))


def pdf_to_text(pdf_filename, to_text=False):
    """Convert PDF from given filename to raw text.

    Save file content into txt file if specified.
    """

    # Load PDF into raw text:
    with open(pdf_filename, "rb") as f:
        pdf = pdftotext.PDF(f)
        pdf_txt = "\n\n".join(pdf)

    # If specified, save PDF into txt:
    if to_text:
        with open(pdf_filename[:-4] + '.txt', "w") as f:
            f.write(pdf_txt)
    return pdf_txt


def extract_contracts(pdf_filename, to_text=False, cont_list=False):
    """Extract contract codes from given PDFs."""

    # Set contract (regular expression) rule:
    regex = r'[A-Za-z]+\/[A-Za-z]+\/[A-Za-z0-9]+\/[A-Za-z0-9]+\/[A-Za-z0-9]+'
    extractor = re.compile(regex)

    # Find all contracts in PDF file:
    pdf_txt = pdf_to_text(pdf_filename, to_text)
    contracts_raw = extractor.findall(pdf_txt)
    contracts = "\n".join(contracts_raw)

    # If specified, save output list:
    if cont_list:
        with open(pdf_filename[:-4] + '_contratos.txt', "w") as f:
            f.write(contracts)

    return contracts


def extract_from_dir(dir_path, to_text=False, con_list=False):
    """Contracts extractor from given directory."""

    pdfs_w_contracts = 0
    pdf_list = list_pdfs(dir_path)
    for pdf in pdf_list:
        contracts = extract_contracts(pdf, to_text, con_list)
        if len(contracts) > 0:
            pdfs_w_contracts += 1

    if pdfs_w_contracts > 0:
        output_message = "Contracts found in {} PDFs!".format(pdfs_w_contracts)
    else:
        output_message = "No contracts found in this directory!"
    return output_message


if __name__ == '__main__':
    # pdf_list = list_pdfs("../y_2017")
    # print(extract_contracts(pdf_list[0]))
    print(extract_from_dir("../y_2017", con_list=True))
