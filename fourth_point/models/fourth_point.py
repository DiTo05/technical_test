from odoo import models, fields, api
from collections import defaultdict


class FourthPoint(models.Model):
    _name = 'fourth.point'
    _description = "Clase cuarto punto"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Char('Secuencia', readonly=True, index=True, copy=False, default='Nuevo', help="Secuencia generado de forma automatica")
    products_ids = fields.One2many('product', 'fourth_point_id', sreing="Productos", required=True, tracking=True, help="Campo relacional Uno a Muchos")
    result = fields.Text('Resultado', readonly=True, help="Resultado generado automaticamente")

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('fourth.point')
        return super(FourthPoint, self).create(vals)

    def action_txt_to_result(self):
        for r in self:
            if r.products_ids:
                dict = {}
                dict_genders = {}
                dict_category = {}
                list_products = []
                list_genders = []
                list_category = []
                list_marker = r.mapped('products_ids.marker')
                list_marker = list(set(list_marker))
                for marker in list_marker:
                    for line in r.products_ids:
                        if line.marker == marker:
                            list_category.append(line.category)
                    list_category = list(set(list_category))
                    for category in list_category:
                        for line in r.products_ids:
                            if line.category == category and line.marker == marker:
                                list_genders.append(line.genders)
                        list_genders = list(set(list_genders))
                        for genders in list_genders:
                            for line in r.products_ids:
                                if line.genders == genders and line.category == category and line.marker == marker:
                                    list_products.append([line.name, line.code])
                                print(list_products)
                                dict_genders.update({genders: list_products})
                            list_products = []
                            print(list_genders)
                            dict_category.update({category: dict_genders})
                        list_genders = []
                        dict_genders = {}
                        print(list_category)
                        dict.update({marker: dict_category})
                    list_category = []
                    dict_category = {}
                r.result = dict

