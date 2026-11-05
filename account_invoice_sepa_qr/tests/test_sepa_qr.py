# Copyright 2026 Biricon IT Services GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import Command
from odoo.tests import TransactionCase, tagged

from .. import post_init_hook

COMPANY_IBAN = "AT611904300234573201"
CUSTOMER_IBAN = "DE89370400440532013000"


@tagged("post_install", "-at_install")
class TestSepaQr(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.journal = cls.env["account.journal"].search(
            [("type", "=", "sale"), ("company_id", "=", cls.company.id)], limit=1)
        cls.income_account = cls.env["account.account"].search([("account_type", "=", "income")], limit=1)
        cls.eur = cls.env.ref("base.EUR")
        cls.eur.active = True  # the SEPA code only exists for euro invoices
        cls.partner_a = cls.env["res.partner"].create({"name": "SEPA QR Test Customer"})
        cls.company.qr_code = True
        cls.company_bank = cls.env["res.partner.bank"].create({
            "acc_number": COMPANY_IBAN,
            "partner_id": cls.company.partner_id.id,
            "allow_out_payment": True,
        })
        cls.customer_bank = cls.env["res.partner.bank"].create({
            "acc_number": CUSTOMER_IBAN,
            "partner_id": cls.partner_a.id,
        })

    def _invoice(self):
        if not self.journal:
            self.skipTest("no chart of accounts in this database")
        invoice = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.partner_a.id,
            "invoice_date": "2026-11-05",
            "journal_id": self.journal.id,
            "currency_id": self.eur.id,
            "invoice_line_ids": [Command.create({"name": "Service", "quantity": 2, "price_unit": 100.0,
                                                  "account_id": self.income_account.id})],
        })
        invoice.action_post()
        return invoice

    def _html(self, invoice):
        html, _fmt = self.env["ir.actions.report"]._render_qweb_html("account.account_invoices", invoice.ids)
        return html.decode()

    def test_qr_is_printed_without_anything_on_top(self):
        invoice = self._invoice()
        invoice.partner_bank_id = self.company_bank
        html = self._html(invoice)
        self.assertIn("o_sepa_qr", html)
        self.assertIn('src="data:image/png;base64,', html.split("o_sepa_qr")[0][-200:] + html.split("o_sepa_qr")[1][:200])
        self.assertNotIn("qrcode_odoo_logo", html, "nothing may cover the code")
        self.assertIn("o_sepa_qr", html)
        self.assertIn("padding: 3mm", html, "a quiet zone around the code")

    def test_qr_never_pays_somebody_else(self):
        invoice = self._invoice()
        # directly in the database: other modules may refuse foreign accounts on invoices, but imported ones exist
        self.env.cr.execute("UPDATE account_move SET partner_bank_id = %s WHERE id = %s",
                            (self.customer_bank.id, invoice.id))
        invoice.invalidate_recordset(["partner_bank_id"])
        self.assertEqual(invoice.partner_bank_id, self.customer_bank)
        html = self._html(invoice)
        self.assertNotIn("o_sepa_qr", html, "no code for a foreign account")

    def test_no_qr_for_paid_invoice(self):
        invoice = self._invoice()
        invoice.partner_bank_id = self.company_bank
        if not self.env["account.journal"].search([("type", "=", "bank"), ("company_id", "=", self.company.id)]):
            self.skipTest("no bank journal in this database")
        self.env["account.payment.register"].with_context(
            active_model="account.move", active_ids=invoice.ids).create({}).action_create_payments()
        self.assertFalse(invoice.amount_residual)
        self.assertNotIn("o_sepa_qr", self._html(invoice))

    def test_post_init_hook_switches_the_setting_on(self):
        self.company.qr_code = False
        post_init_hook(self.env)
        self.assertTrue(self.company.qr_code)
