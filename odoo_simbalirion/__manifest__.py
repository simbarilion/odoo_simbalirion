# noinspection PyStatementEffect
{
    "name": "Odoo simbalirion Custom Sale",
    "version": "1.0",
    "summary": "Добавляет обязательное поле сотрудника и поле New Field в Quotation",
    "category": "Sales",
    "depends": ["sale", "hr"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "reports/report_saleorder.xml",
    ],
    "installable": True,
    "application": False,
}
