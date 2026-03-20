# noinspection PyStatementEffect
{
    "name": "Odoo simbalirion Custom Sale v10",
    "version": "1.0",
    "summary": "Добавляет обязательное поле сотрудника и поле New Field в Quotation",
    "category": "Sales",
    "depends": ["sale", "hr"],
    "data": [
        "views/sale_order_views.xml",
        "reports/report_saleorder.xml",
    ],
    "installable": True,
    "application": True,
}
