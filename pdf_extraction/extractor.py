from glob import glob
import pandas as pd
import pdftotext
import re

# Global:
path_to_pdfs = "../y_2017"


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


def extract_from_contracts(pdf_filename, to_text=False, cont_list=False):
    """Extract contract codes from given PDFs."""

    # Set contract rules:
    cn_re = r'[A-Za-z]+\/[A-Za-z]+\/[A-Za-z0-9]+\/[A-Za-z0-9]+\/[A-Za-z0-9]+'
    ta_re = r'Auditoría (.*?): (.*?)\n(.*?)\n'
    ta_re_nl = r'Auditoría (.*?): (.*?)\n(.*?)\n(.*?)\n'
    contract_ext = re.compile(cn_re)
    meta_ext = re.compile(ta_re)
    meta_ext2 = re.compile(ta_re_nl)

    # Find all contracts in PDF file:
    pdf_txt = pdf_to_text(pdf_filename, to_text)
    pdf_txt = re.sub('"', '\"', pdf_txt)
    pdf_txt = re.sub("'", "\'", pdf_txt)
    contracts_raw = contract_ext.findall(pdf_txt)
    meta_raw = meta_ext.findall(pdf_txt)
    contracts = list(set(contracts_raw))

    try:
        if 'GB' in meta_raw[0][2] or 'DS' in meta_raw[0][2] or \
           'DE' in meta_raw[0][2] or 'GF' in meta_raw[0][2]:
            pass
        else:
            meta_raw = meta_ext2.findall(pdf_txt)
            meta_raw = [(meta_raw[0][0], meta_raw[0][1] +
                         meta_raw[0][2], meta_raw[0][3])]
    except Exception as e:
        pass

    try:
        meta = [item for item in meta_raw[0]]
    except Exception as e:
        meta = []

    # If specified, save output list:
    if cont_list:
        with open(pdf_filename[:-4] + '_contratos.txt', "w") as f:
            f.write(contracts)

    return meta, contracts, pdf_txt


def extract_from_dir(dir_path, to_text=False, con_list=False, out="out.csv"):
    """Contracts extractor from given directory."""

    # Create empty arrays:
    columnas = ['id_auditoria', 'numero', 'nombre_archivo', 'tipo_auditoria',
                'contratos', 'contenido_crudo']
    data = []

    # Iterate over pdfs:
    pdfs_w_contracts = 0
    pdf_list = list_pdfs(dir_path)
    for i, pdf in enumerate(pdf_list):
        print("Processing PDF {} of {}.".format(i, len(pdf_list)))
        meta, contracts, pdf_txt = extract_from_contracts(
            pdf, to_text, con_list)
        filename = pdf.split("/")[-1]
        try:
            vector = [meta[1], meta[2], filename, meta[0], contracts, pdf_txt]
            data.append(vector)
            if len(contracts) > 0:
                pdfs_w_contracts += 1
        except Exception as e:
            data.append([None, None, filename, None, contracts, pdf_txt])

    df = pd.DataFrame(data, columns=columnas)
    df.to_csv(out)

    # if pdfs_w_contracts > 0:
    #     output_message = "{} contracts found!".format(pdfs_w_contracts)
    # else:
    #     output_message = "No contracts found in this directory!"

    return df


if __name__ == '__main__':
    # pdf_list = list_pdfs(path_to_pdfs)
    # print(extract_from_contracts(pdf_list[0])[:2])
    print(extract_from_dir("../y_2017"))
