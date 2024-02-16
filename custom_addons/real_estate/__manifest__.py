{
    'name': "Real Estate Ads",
    'version': "1.0.0",
    'website': "https://www.google.com",
    'description': """
        Real Estate Module Description
""",
    'author': "Dave",
    'depends': ['base'],
    'category': "Sales",
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_tag.xml',
        'views/menu_items.xml'
    ],
    'license': "LGPL-3",
    'web_icon': "real_estate/static/description/icon.png"
}