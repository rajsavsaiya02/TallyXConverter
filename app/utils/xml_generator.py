# app/utils/xml_generator.py
import pandas as pd
from lxml import etree


def generate_tally_xml(df: pd.DataFrame) -> bytes:
    """
    Generates Tally-compliant XML from a DataFrame.
    lxml.etree is used for optimal performance.
    """
    envelope = etree.Element("ENVELOPE")
    header = etree.SubElement(envelope, "HEADER")
    etree.SubElement(header, "TALLYREQUEST").text = "Import Data"
    body = etree.SubElement(envelope, "BODY")
    import_data = etree.SubElement(body, "IMPORTDATA")
    request_desc = etree.SubElement(import_data, "REQUESTDESC")
    etree.SubElement(request_desc, "REPORTNAME").text = "Vouchers"

    request_data = etree.SubElement(import_data, "REQUESTDATA")

    for index, row in df.iterrows():
        tally_message = etree.SubElement(request_data, "TALLYMESSAGE", {"xmlns:UDF": "TallyUDF"})
        voucher = etree.SubElement(tally_message, "VOUCHER")
        etree.SubElement(voucher, "DATE").text = str(row['Date'])
        etree.SubElement(voucher, "PARTYLEDGERNAME").text = str(row['Party'])
        etree.SubElement(voucher, "VOUCHERTYPENAME").text = "Sales"

        # Debtor Entry
        all_ledger_entries_dr = etree.SubElement(voucher, "ALLLEDGERENTRIES.LIST")
        etree.SubElement(all_ledger_entries_dr, "LEDGERNAME").text = str(row['Party'])
        etree.SubElement(all_ledger_entries_dr, "ISDEEMEDPOSITIVE").text = "Yes"
        etree.SubElement(all_ledger_entries_dr, "AMOUNT").text = str(row['Amount'])

        # Sales Ledger Entry
        all_ledger_entries_cr = etree.SubElement(voucher, "ALLLEDGERENTRIES.LIST")
        etree.SubElement(all_ledger_entries_cr, "LEDGERNAME").text = "Sales"
        etree.SubElement(all_ledger_entries_cr, "ISDEEMEDPOSITIVE").text = "No"
        etree.SubElement(all_ledger_entries_cr, "AMOUNT").text = str(-row['Amount'])  # Negative for credit

    # Pretty print is off for production to minimize payload size
    return etree.tostring(envelope, pretty_print=False)