from odoo import models, fields, api, tools

class Cliente(models.Model):
    _name = 'gestion_pedidos.cliente'
    _description = 'Cliente'

    name = fields.Char(string='Nombre', required=True)
    email = fields.Char(string='Email')
    telefono = fields.Char(string='Teléfono')
    direccion = fields.Text(string='Dirección')
    pedidos_ids = fields.One2many('gestion_pedidos.pedido', 'cliente', string='Pedidos')

class Producto(models.Model):
    _name = 'gestion_pedidos.producto'
    _description = 'Producto'

    name = fields.Char(string='Nombre', required=True)
    descripcion = fields.Text(string='Descripción')
    precio = fields.Float(string='Precio', required=True)
    lineas_pedido_ids = fields.One2many('gestion_pedidos.linea_pedido', 'producto_id', string='Líneas de Pedido')

class Pedido(models.Model):
    _name = 'gestion_pedidos.pedido'
    _description = 'Gestión de Pedidos'
    _inherit = ['mail.thread']
    _order = 'fecha_pedido desc'

    name = fields.Char(string='Nombre', required=True)
    fecha_pedido = fields.Date(string='Fecha del Pedido', default=fields.Date.today)
    cliente = fields.Many2one('gestion_pedidos.cliente', string='Cliente', required=True)
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado')
    ], string='Estado', default='borrador')
    lineas_pedido = fields.One2many('gestion_pedidos.linea_pedido', 'pedido_id', string='Líneas de Pedido')
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    mes_pedido = fields.Char('Mes', compute='_compute_mes_pedido', store=True)

    @api.depends('lineas_pedido.subtotal')
    def _compute_total(self):
        for pedido in self:
            pedido.total = sum(linea.subtotal for linea in pedido.lineas_pedido)

    @api.depends('fecha_pedido')
    def _compute_mes_pedido(self):
        for record in self:
            if record.fecha_pedido:
                record.mes_pedido = record.fecha_pedido.strftime('%B %Y')
            else:
                record.mes_pedido = False

    def action_draft(self):
        self.write({'estado': 'borrador'})

    def action_confirm(self):
        self.write({'estado': 'confirmado'})

    def action_deliver(self):
        self.write({'estado': 'entregado'})

    def action_cancel(self):
        self.write({'estado': 'cancelado'})

    def init(self):
        tools.create_index(self._cr, 'pedido_fecha_estado_idx', 
                          self._table, ['fecha_pedido', 'estado'])

class LineaPedido(models.Model):
    _name = 'gestion_pedidos.linea_pedido'
    _description = 'Línea de Pedido'

    pedido_id = fields.Many2one('gestion_pedidos.pedido', string='Pedido')
    producto_id = fields.Many2one('gestion_pedidos.producto', string='Producto', required=True)
    cantidad = fields.Float(string='Cantidad', default=1.0)
    precio_unitario = fields.Float(string='Precio Unitario')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('cantidad', 'precio_unitario')
    def _compute_subtotal(self):
        for linea in self:
            linea.subtotal = linea.cantidad * linea.precio_unitario