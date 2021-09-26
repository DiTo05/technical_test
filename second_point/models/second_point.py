from odoo import models, fields, api
import cmath


class SecondPoint(models.Model):
    _name = 'complex'
    _description = "Clase segundo punto"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Char('Secuencia', readonly=True, index=True, copy=False, default='Nuevo')
    first_value_a = fields.Float('Primer valor A', required=True, digits=(12,2))
    second_value_a = fields.Float('Segundo valor A', required=True, digits=(12,2))
    first_value_b = fields.Float('Primer valor B', required=True, digits=(12,2))
    second_value_b = fields.Float('Segundo valor B', required=True, digits=(12,2))
    sum = fields.Char('A + B', readonly=True, help="Resultado suma")
    subtraction = fields.Char('A - B', readonly=True, help="Resultado resta")
    multiplication = fields.Char('A * B', readonly=True, help="Resultado multiplicación")
    division = fields.Char('A / B', readonly=True, help="Resultado división")
    module_a = fields.Char('Mod (A)', readonly=True, help="Resultado modulo A")
    module_b = fields.Char('Mod (B)', readonly=True, help="Resultado modulo B")

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('complex')
        return super(SecondPoint, self).create(vals)

    def action_txt_to_result(self):
        for r in self:
            if r.first_value_a and r.first_value_a and r.second_value_a and r.second_value_b:
                first = complex(r.first_value_a, r.second_value_a)
                second = complex(r.first_value_b, r.second_value_b)
                r.sum = str(first + second)
                r.subtraction = str(first - second)
                r.multiplication = str(first * second)
                div = first / second
                r.division = complex(round(div.real, 4), round(div.imag, 4))
                r.module_a = str(complex(round(abs(first), 4), 0.00))
                r.module_b = str(complex(round(abs(second), 4), 0.00))
