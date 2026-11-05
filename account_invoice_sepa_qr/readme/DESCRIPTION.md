Prints the **SEPA transfer QR code** (EPC "GiroCode") on customer invoices, so that customers can pay by scanning it
with their banking app. Amount, payment reference and account of your company are already filled in.

Odoo already has this feature (standard module *SEPA QR Code*, setting "Display SEPA QR-code"), but in the standard
report it is switched off, and when it is on

* the Odoo logo sits in the middle of the code and covers modules of it,
* the code has no white margin, so a neighbouring line of text can disturb the scan,
* the code is printed for whatever bank account is stored on the invoice - after migrations or imports that is
  often the account of the *customer*, which would make the customer pay himself.

This module switches the setting on at installation and fixes the three points.
