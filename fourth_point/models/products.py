from odoo import models, fields


class Product(models.Model):
    _name = 'product'
    _description = "Clase relacional cuarto punto"

    fourth_point_id = fields.Many2one('fourth.point', help="Campo relacionar Muchos a Uno", readonly=True)
    name = fields.Char('Nombre', help="Nombre del producto", required=True)
    code = fields.Char('Código de barras', help="Codigo de barras del producto", required=True)
    marker = fields.Char('Fabricante', help="Fabricante del producto", required=True)
    category = fields.Char('Categoría', help="Categoria del producto", required=True)
    genders = fields.Selection([('Masculino', 'Masculino'), ('Femenino', 'Femenino')], 'Género', help="Genero del producto", required=True)
