{
    'name': "billing_generation",
    'version': '1.0',
    'summary': 'Bill Generation',
    'depends': ['base' , 'sale' , 'sale_management' , 'project' , 'product'],
    'author':"komal",
    'description': """
    Description text
    """,

    "data": [
        "security/ir.model.access.csv",
        "views/quotation_view.xml",
        "views/billing_menuitem.xml",
    ],

    'category': 'billing_generation/billing_generation',
    'website': 'https://www.odoo.com/app/billing_generation',
}