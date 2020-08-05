# Copyright 2008 Luis Falcon <falcon@gnuhealth.org>
# Copyright 2016 LasLabs Inc.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from datetime import date, datetime
from odoo import _, api, fields, models
from odoo.modules import get_module_resource
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError


class MedicalPatient(models.Model):
    _name = 'medical.patient'
    _description = 'Medical Patient'
    _inherit = 'medical.abstract.entity'

    age = fields.Char(
        compute='_compute_age',
        string="Age (computed)"
    )
    age_years = fields.Integer(
        string="Age",
        compute='_compute_age',
        search='_search_age',
    )
    identification_code = fields.Char(
        string='Identificación interna',
        help='Identificación del paciente provista por el centro de salud',
    )
    general_info = fields.Text(
        string='Información General',
    )
    is_deceased = fields.Boolean(
        compute='_compute_is_deceased',
    )
    marital_status = fields.Selection(
        [
            ('s', 'Single'),
            ('m', 'Married'),
            ('w', 'Widow(er)'),
            ('d', 'Divorced'),
            ('x', 'Separated')
        ]
    )
    is_pregnant = fields.Boolean(
        help='¿Esta embarazada?',
    )
    date_death = fields.Datetime(
        string='Deceased date',
    )

    def _compute_age(self):
        """ Age computed based on the birth date in the membership request."""
        now = datetime.now()
        for record in self:
            if record.birthdate_date:
                birthdate_date = fields.Datetime.from_string(
                    record.birthdate_date,
                )
                if record.is_deceased:
                    date_death = fields.Datetime.from_string(record.date_death)
                    delta = relativedelta(date_death, birthdate_date)
                    is_deceased = _(' (deceased)')
                else:
                    delta = relativedelta(now, birthdate_date)
                    is_deceased = ''
                years_months_days = '%d %s' % (
                    delta.years, is_deceased
                )
                years = delta.years
            else:
                years_months_days = _('No DoB')
                years = False
            record.age = years_months_days
            if years:
                record.age_years = years

    def _compute_is_deceased(self):
        for record in self:
            record.is_deceased = bool(record.date_death)

    @api.constrains('is_pregnant', 'gender')
    def _check_is_pregnant(self):
        for record in self:
            if record.is_pregnant and record.gender != 'female':
                raise ValidationError(_(
                    'Invalid selection - Only a `Female` may be pregnant.',
                ))

    @api.model
    def _create_vals(self, vals):
        vals = super(MedicalPatient, self)._create_vals(vals)
        if not vals.get('identification_code'):
            Seq = self.env['ir.sequence']
            vals['identification_code'] = Seq.sudo().next_by_code(
                self._name,
            )
        # vals.update({
        #     'customer': True,
        # })
        return vals

    def _get_default_image_path(self, vals):
        super(MedicalPatient, self)._get_default_image_path(vals)
        return get_module_resource(
            'medical', 'static/src/img', 'patient-avatar.png'
        )

    def _search_age(self, operator, value):
        if operator not in ('ilike', '=', '>=', '>', '<', '<='):
            raise UserError(_('Invalid operator: %s' % (operator,)))

        current_date = date.today()
        last_birthdate = current_date + relativedelta(years=value * -1)
        first_birthdate = current_date + relativedelta(
            years=(value + 1) * -1, days=1
        )
        last_possible_birthdate = fields.Datetime.to_string(last_birthdate)
        first_possible_birthdate = fields.Datetime.to_string(first_birthdate)

        if operator == '=' or operator == 'ilike':
            return [
                '&', ('birthdate_date', '>=', first_possible_birthdate),
                ('birthdate_date', '<=', last_possible_birthdate)
            ]
        elif operator == '>=':
            return [('birthdate_date', '<=', last_possible_birthdate)]
        elif operator == '>':
            return [('birthdate_date', '<', first_possible_birthdate)]
        elif operator == '<=':
            return [('birthdate_date', '>=', first_possible_birthdate)]
        elif operator == '<':
            return [('birthdate_date', '>', last_possible_birthdate)]

    def toggle_is_pregnant(self):
        self.toggle('is_pregnant')

    def toggle_safety_cap_yn(self):
        self.toggle('safety_cap_yn')

    def toggle_counseling_yn(self):
        self.toggle('counseling_yn')
