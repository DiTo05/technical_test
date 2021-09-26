from odoo import models, fields, api
from odoo.exceptions import UserError
import requests

CLIENT_ID = '6e31e281a4fa44c6ba44045368bbbb82'
CLIENT_SECRET = '47a8e023c9554575bd58246911c5e06f'
AUTH_URL = 'https://accounts.spotify.com/api/token'


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = "Clase cliente SPOTIFY"

    fifth_point_ids = fields.One2many('fifth.point', 'customer_id', string='Historial canciones spotify')
    sequence = fields.Char('Secuencia', readonly=True, index=True, copy=False, default='Nuevo', help="Secuencia generado de forma automatica")
    category_song_ids = fields.Many2many('song.tag.category', string="Categorias", required=True, ondelete='cascade')

    @api.constrains('category_song_ids')
    def api_spotify(self):
        for record in self:
            if record.category_song_ids:
                # POST
                auth_response = requests.post(AUTH_URL, {
                    'grant_type': 'client_credentials',
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                })
                auth_response_data = auth_response.json()
                access_token = auth_response_data['access_token']
                headers = {
                    'Authorization': 'Bearer {token}'.format(token=access_token)
                }
                BASE_URL = 'https://api.spotify.com/v1/'
                r = requests.get(BASE_URL + 'recommendations/available-genre-seeds' , headers=headers)
                r = r.json()

                for category in record.category_song_ids:
                    if category.name not in r.get('genres'):
                        raise UserError('El genero %s no existe en Spotify.' % category.name)
                    else:
                        track = requests.get(BASE_URL + 'search?q=' + category.name + '&type=track', headers=headers)
                        track = track.json()
                        record.fifth_point_ids = [(0, 0, {
                            'name': track.get('tracks').get('items')[1].get('name'),
                            'url': track.get('tracks').get('items')[1].get('external_urls').get('spotify'),
                            'category': track.get('tracks').get('items')[0].get('name')
                        })]


class SongTagCategory(models.Model):
    _name = 'song.tag.category'
    _description = "SOng Tag Category"

    name = fields.Char("Nombre", required=True, translate=True)