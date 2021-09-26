from odoo import models, fields, api
from odoo.addons.base.models.res_partner import _tz_get
from datetime import datetime
from pytz import timezone, UTC, utc


class ThirdPoint(models.Model):
    _name = 'third.point'
    _description = "Clase tercer punto"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Char('Secuencia', readonly=True, index=True, copy=False, default='Nuevo', help="Secuencia generado de forma automatica")
    first_date = fields.Datetime('Primera fecha', required=True, tracking=True, help="Primera fecha")
    second_date = fields.Datetime('Segunda fecha', required=True, tracking=True, help="Segunda fecha")
    first_tz = fields.Selection(_tz_get, string='Zona horaria primera fecha', required=True, default="America/Bogota")
    second_tz = fields.Selection(_tz_get, string='Zona horaria segunda fecha', required=True, default="America/Bogota")
    result_hours = fields.Float('Horas laborales', readonly=True, tracking=True, help="Campo solo lectura, expresa solución a la operación cargada")
    resource_calendar_id = fields.Many2one('resource.calendar', 'Calendario laboral', required=True, domain="[('name', '=', 'Colombian 40 hours/week')]")
    result_days = fields.Integer('Cantidad días', readonly=True, tracking=True, help="Campo solo lectura, expresa solución a la operación cargada")
    result_dates = fields.Char('Diferencia fechas', readonly=True, tracking=True, help="Campo solo lectura, expresa solución a la operación cargada")

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('third.point')
        return super(ThirdPoint, self).create(vals)

    def action_txt_to_result(self):
        count_hours = 0

        first_date = self.first_date.replace(tzinfo=UTC).astimezone(timezone(self.first_tz)).replace(tzinfo=None)
        second_date = self.second_date.replace(tzinfo=UTC).astimezone(timezone(self.second_tz)).replace(tzinfo=None)

        if first_date and second_date:
            if first_date.weekday() != [6, 7]:
                if first_date.hour <= 8:
                    count_hours += 8
                elif first_date.hour >= 16:
                    count_hours += 0
                else:
                    print(16 - first_date.hour)
                    count_hours += 16 - first_date.hour
                    count_hours += 16 - first_date.hour
            if second_date.weekday() != [6, 7]:
                if second_date.hour <= 8:
                    count_hours += 8
                elif second_date.hour >= 16:
                    count_hours += 0
                else:
                    count_hours += second_date.hour - 8
                    print(second_date.hour - 8)
            if ((second_date.day - first_date.day) - 1) > 0:
                for i in range(0, (second_date.day - first_date.day) - 1):
                    first_date.day + 1
                    if first_date.weekday() != [6, 7]:
                        count_hours += 8
        self.result_hours = count_hours
        self.result_days = second_date.day - first_date.day + 1
        self.result_dates = second_date - first_date



