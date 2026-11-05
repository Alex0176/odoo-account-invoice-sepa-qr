# Copyright 2026 Biricon IT Services GmbH
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).


def post_init_hook(env):
    """Switch on "Display SEPA QR-code" (Accounting settings) for all companies."""
    env["res.company"].search([("qr_code", "=", False)]).write({"qr_code": True})
