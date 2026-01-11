from marshmallow import Schema, fields

class DailyMetricSchema(Schema):
    id = fields.Int()
    asset_id = fields.Int()
    date = fields.Date()
    energy_mwh = fields.Float()
    availability_pct = fields.Float()
