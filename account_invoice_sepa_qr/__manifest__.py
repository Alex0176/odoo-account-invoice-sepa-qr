# Copyright 2026 Biricon IT Services GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Invoices with SEPA Payment QR Code",
    "summary": "Prints the SEPA transfer QR code (EPC) on customer invoices without anything covering it, "
    "and only for the bank account of your own company",
    "version": "19.0.1.0.0",
    "category": "Accounting/Accounting",
    "author": "Biricon IT Services GmbH",
    "website": "https://github.com/Alex0176/odoo-account-invoice-sepa-qr",
    "license": "LGPL-3",
    "depends": ["account", "account_qr_code_sepa"],
    "data": ["views/report_invoice.xml"],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
