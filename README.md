# Odoo Account Invoice SEPA QR

Odoo 19.0 addon by **Biricon IT Services GmbH** (LGPL-3).

| Module | Description |
|---|---|
| [account_invoice_sepa_qr](account_invoice_sepa_qr/) | Prints the SEPA transfer QR code (EPC "GiroCode") on customer invoices: nothing covers the code, it has a white margin, and it is only printed for an active bank account of your own company. |

## What it does

Odoo's standard report can print the SEPA QR code, but

- the Odoo logo is drawn over the middle of the code,
- the code has no white margin, a neighbouring line of text can disturb the scan,
- it is printed for whatever bank account is stored on the invoice. After migrations or imports that is often the
  account of the *customer*, so the customer would pay himself.

This module switches *Display SEPA QR-code* on for all companies at installation and fixes the three points. It does
not change the layout of the invoice otherwise, and it also works with report layouts that copy the standard invoice
block (the last matching block is changed).

No code is printed for paid invoices, for other currencies than EUR, for non-SEPA accounts, and when the bank account
of the invoice does not belong to your company.

## Requirements

- Odoo 19.0 with the standard modules `account` and `account_qr_code_sepa`

## Installation

1. Put `account_invoice_sepa_qr` into the addons path.
2. Update the apps list and install *Invoices with SEPA Payment QR Code*.
3. Switch it off again, if wanted, in *Accounting > Settings > Customer Payments > Display SEPA QR-code*.

The installation changes the report view only. German translation included.

## Tests

```
odoo-bin -d <database> -i account_invoice_sepa_qr --test-tags /account_invoice_sepa_qr --stop-after-init
```

## License

LGPL-3.0 or later, see [LICENSE](LICENSE).
