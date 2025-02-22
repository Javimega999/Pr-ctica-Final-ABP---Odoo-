# -*- coding: utf-8 -*-
{
    'name': "Gestión de Pedidos",
    'summary': "Módulo para gestionar pedidos de clientes",
    'description': """
        Módulo que permite gestionar:
        - Pedidos
        - Líneas de pedido
        - Estados de pedido
    """,
    'author': "Your Company",
    'website': "https://www.yourcompany.com",
    'category': 'Sales',
    'version': '2.0',
    'depends': ['base', 'sale_management', 'product'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'reports/factura_report.xml',
        'views/pedido_views.xml',
        'views/menus.xml',
    ],
    'application': True,
    'installable': True,
}

