from odoo import models, fields, api


class FifthPoint(models.Model):
    _name = 'fifth.point'
    _description = "Clase quinto punto"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    customer_id = fields.Many2one('res.partner', string='Cliente')
    name = fields.Char('Nombre', help="Nombre de la canción recomendada")
    url = fields.Char('URL', help="URL de la canción recomendada")
    category = fields.Char('Categoria', help="Categoria de la canción")
