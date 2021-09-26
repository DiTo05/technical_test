from odoo import models, fields, api, _
import base64
from odoo.exceptions import UserError


class FirstPoint(models.Model):
    _name = 'first.point'
    _description = "Clase primer punto"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Char('Secuencia', readonly=True, index=True, copy=False, default='Nuevo', help="Secuencia generado de forma automatica")
    name = fields.Char('Nombre ejercicio', required=True, tracking=True, help="Nombre al actual record, generar registro")
    txt = fields.Binary('Archivo txt', attachment=True, tracking=True, help="Anexe el archivo .txt correspondiente a al punto uno")
    txt_filename = fields.Char('Nombre txt', readonly=True, tracking=True, help="Nombre archivo txt")
    result = fields.Text('Resultado', readonly=True, tracking=True, help="Campo solo lectura, expresa solución a la operación cargada")
    result_file = fields.Binary('Resultado .bin', readonly=True, tracking=True, help="Automaticamente se genera un archivo txt correspondiente a la respuesta")

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('first.point')
        return super(FirstPoint, self).create(vals)

    def action_txt_to_result(self):
        if self.txt:
            if '.txt' not in self.txt_filename:
                raise UserError('Formato invalido, es necesario adjuntar un archivo en formato .txt')
            else:
                file = open("Resultado.txt", "w")

                file_content = base64.decodestring(self.txt)
                file_content = file_content.decode("utf-8")
                file_lines = file_content.split("\r\n") and file_content.replace("\n", "")
                words = file_lines.split()
                words.pop(0)
                result = ""
                file_result = open('/odoo/odoo-server/addons/first_point/static/txt/Resultado.txt', 'r+')
                result += str((len(set(words)))) + "\n"
                file_result.write(str((len(set(words)))) + "\n")
                resultantList = []
                for element in words:
                    if element not in resultantList:
                        resultantList.append(element)
                for line in resultantList:
                    result += str(words.count(line)) + " "
                    file_result.write(str(words.count(line)) + " ")
                file_result.close()
                file_result = open('/odoo/odoo-server/addons/first_point/static/txt/Resultado.txt', 'rb')
                self.result_file = base64.b64encode(file_result.read())
                file_result.close()
                self.result = result

                action = {
                    'close_on_report_download': True,
                    'type': 'ir.actions.act_url',
                    'name': 'Resultado.txt',
                    'url': '/web/content/first.point/%s/result_file/Resultado.txt?download=true' % (self.id),
                    }
                return action