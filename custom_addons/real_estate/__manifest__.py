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
        'views/property_offer_view.xml',
        'views/menu_items.xml',
        'data/property.type.csv'
        # 'data/property_type.xml'
    ],
    'demo':[
        'demo/property_tags.xml'
    ],
    'license': "LGPL-3",
    'web_icon': "real_estate/static/description/icon.png"
}