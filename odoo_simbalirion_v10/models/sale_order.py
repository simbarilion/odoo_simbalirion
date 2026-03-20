import random
import string

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    """
    Модель коммерческого предложения: добавление полей:
    - Ответственный за выдачу товара
    - New Field
    """
    _inherit = "sale.order"

    responsible_employee_id = fields.Many2one(
        "hr.employee", string="Ответственный за выдачу товара", required=True
    )
    new_field = fields.Char(
        string="New Field",
        default=lambda self: "".join(random.choices(string.ascii_letters, k=10)),
    )

    new_field_auto_generated = fields.Boolean(
        string="New Field is Auto",
        default=True,
    )

    @api.constrains("new_field")
    def _check_new_field_length(self):
        """
        Проверяет длину текста: если пользователь вводит более 30 символов, выдает
        предупреждение и не позволяет сохранить запись
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
            if not order.new_field_auto_generated:
                continue  # пользователь уже редактировал вручную
            date_str = ""
            if order.date_order:
                date_str = order.date_order.strftime("%d/%m/%Y %H:%M:%S")
            total = order.amount_total or 0.0
            new_val = f"{date_str} + {total:.2f}"
            if order.new_field != new_val:
                order.new_field = new_val

    @api.onchange("new_field")
    def _onchange_new_field_manual(self):
        """
        Изменяет значение поля new_field_auto_generated:
        если пользователь изменил поле вручную, снимает флаг авто
        """
        for order in self:
            if order.state == "draft":
                order.new_field_auto_generated = False
