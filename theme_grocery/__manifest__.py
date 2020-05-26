# -*- coding: utf-8 -*-
# Copyright (C) Kanak Infosystems LLP.

{
    'name': 'Theme Grocery',
    'version': '1.0',
    'summary': 'One of the finest website ecommerce theme which suits many nature of businesses out of box',
    'description': """
Theme Grocery
==============
Online Supermarket includes on-line vegetable store, foods and groceries available on-line on-line.
    """,
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'support': 'info@kanakinfosystems.com',
    'category': 'Theme/Grocery',
    'depends': [
        'website_sale_wishlist', 'website_sale_comparison',
        'website_blog', 'website_mass_mailing', 'website_theme_install'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/customize_show_templates.xml',
        'views/h_f_templates.xml',
        'views/homepage_templates.xml',
        'views/shop_templates.xml',
        'views/product_details_templates.xml',
        'views/theme_customise_assets.xml',
        'views/theme_customise_templates.xml',
    ],
    'installable': True,
    'images': [
        'static/description/theme_grocery.jpg',
        'static/description/theme_grocery_screenshot.jpg'
    ],
    'application': True,
    'price': 100,
    'currency': 'EUR',
    'live_test_url': 'http://v11.kanakinfosystems.com/web?db=theme_grocery',
}
