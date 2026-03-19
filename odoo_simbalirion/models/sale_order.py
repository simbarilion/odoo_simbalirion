import random
import string

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    """
    Модель коммерческого предложения: добавление полей:
    - Ответственный за выдачу товара
    - New Field
    """
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

    @api.constrains("new_field")
    def _check_new_field_length(self):
        """
        Проверяет длину текста: если пользователь вводит более 30 символов, выдает предупреждение
        и не позволяет сохранить запись
        """
        for record in self:
            if record.new_field and len(record.new_field) > 30:
                raise ValidationError("Длина текста должна быть меньше 30 символов!")

    @api.onchange("order_line", "date_order")
    def _onchange_update_new_field(self):
        """
        Обновляет поле new_field при изменении строк заказа или даты заказа.
        Не перезаписывает значение, если пользователь ввел текст вручную
        """
        for order in self:
            if order.state != "draft":
                continue
            if order.new_field and "+" not in order.new_field:
                continue       # пользователь ввел вручную
            if order.date_order:
                date_str = order.date_order.strftime("%d/%m/%Y %H:%M:%S")
            else:
                date_str = ""
            total = order.amount_total or 0.0
            order.new_field = f"{date_str} + {total:.2f}"
