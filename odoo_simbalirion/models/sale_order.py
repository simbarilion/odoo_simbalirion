import random
import string

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    responsible_employee_id = fields.Many2one(
        "hr.employee",
        string="Ответственный за выдачу товара",
        required=True
    )
    new_field = fields.Char(
        string="New Field",
        default=lambda self: "".join(random.choices(string.ascii_letters, k=10)),
    )

    # Ограничение длины
    @api.constrains("new_field")
    def _check_new_field_length(self):
        for record in self:
            if record.new_field and len(record.new_field) > 30:
                raise ValidationError("Длина текста должна быть меньше 30 символов!")

    # Автоматическое обновление при изменении даты или позиций
    @api.onchange("order_line", "date_order")
    def _onchange_update_new_field(self):
        for order in self:
            if order.state == 'draft':  # меняем только в draft
                total = order.amount_total
                date_str = order.date_order.strftime("%d/%m/%Y %H:%M:%S") if order.date_order else ''
                order.new_field = f"{date_str} + {total:.2f}"

    # Ограничение доступа в зависимости от статуса
    @api.model
    def fields_view_get(self, view_id=None, view_type="form", toolbar=False, submenu=False):
        res = super(SaleOrder, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                     submenu=submenu)
        if view_type == "form":
            from lxml import etree
            doc = etree.XML(res["arch"])
            for node in doc.xpath("//field[@name='new_field']"):
                for record in self:
                    if record.state == "sale":
                        node.set("invisible", "1")
                    elif record.state == "sent":
                        node.set("readonly", "1")
                    else:
                        node.set("readonly", "0")
            res["arch"] = etree.tostring(doc, encoding="unicode")
        return res
