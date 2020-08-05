# -*- coding: utf-8 -*-
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    MODULE : Diagnostic Imaging
#
#    Copyright (C) 2008-2020 Luis Falcon <lfalcon@gnuhealth.org>
#    Copyright (C) 2011-2020 GNU Solidario <health@gnusolidario.org>
#    Copyright (C) 2013  Sebastián Marro <smarro@thymbra.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import datetime
from odoo import models, fields, api

__all__ = [
    'GnuHealthSequences', 'GnuHealthSequenceSetup','ImagingTestType',
    'ImagingTest', 'ImagingTestRequest', 'ImagingTestResult']

sequences = ['imaging_request_sequence', 'imaging_sequence']


class GnuHealthSequences(models.Model ):
    "GNU Health Sequences"
    _name = "gnuhealth.sequences"
    _description = "GNU Health Sequences"
    _order = 'id,name'
    _table = 'gnuhealth_sequences'

    imaging_request_sequence =  fields.Many2one(
        'ir.sequence',
        'Imaging Request Sequence',
        domain=[('code', '=', 'gnuhealth.imaging.test.request')],
        required=True)
    imaging_sequence =   fields.Many2one(
        'ir.sequence',
        'Imaging Sequence',
        domain=[('code', '=', 'gnuhealth.imaging.test.result')],
        required=True)


    @classmethod
    def _multivalue_model(self, field):
        self.env = self.env['gnuhealth.sequence.setup']
        if field in sequences:
            return self.env.get()
        return super(GnuHealthSequences).multivalue_model(field)


    @classmethod
    def _default_imaging_request_sequence(self):
        return self.multivalue_model(
            'imaging_request_sequence').default_imaging_request_sequence()

    @classmethod
    def _default_imaging_sequence(self):
        return self.multivalue_model(
            'imaging_sequence').default_imaging_sequence()

# SEQUENCE SETUP
class GnuHealthSequenceSetup(models.Model):
    'GNU Health Sequences Setup'
    _name = 'gnuhealth.sequence.setup'
    _description = 'GNU Health Sequences Setup'
    _order = 'id,name'
    _table = 'gnuhealth_sequences_setup'

    imaging_request_sequence = fields.Many2one('ir.sequence',
                                               'Imaging Request Sequence', required=True,
                                               domain=[('code', '=', 'gnuhealth.imaging.test.request')])


    imaging_sequence = fields.Many2one('ir.sequence',
                                       'Imaging Result Sequence', required=True,
                                       domain=[('code', '=', 'gnuhealth.imaging.test.result')])

    # @classmethod
    # def __register__(self, module_name):
    #     TableHandler = backend.get('TableHandler')
    #     exist = TableHandler.table_exist(self._table)
    #
    #     super(GnuHealthSequenceSetup, self).__register__(module_name)
    #
    #     if not exist:
    #         self._migrate_property([], [], [])
    #
    # @classmethod
    # def _migrate_property(self, field_names, value_names, fields):
    #     field_names.extend(sequences)
    #     value_names.extend(sequences)
    #     migrate_property(
    #         'gnuhealth.sequences', field_names, self, value_names,
    #         fields=fields)

    @classmethod
    def default_imaging_request_sequence(self):
        ModelData = self.env.get('ir.model.data')
        return ModelData.get_id(
            'health_imaging', 'seq_gnuhealth_imaging_test_request')

    @classmethod
    def default_imaging_sequence(self):
        ModelData = self.env.get('ir.model.data')
        return ModelData.get_id(
            'health_imaging', 'seq_gnuhealth_imaging_test')

# END SEQUENCE SETUP , MIGRATION FROM FIELDS.PROPERTY


class ImagingTestType(models.Model):
    'Imaging Test Type'
    _name = 'gnuhealth.imaging.test.type'
    _description = 'Imaging Test Type'
    _order = 'id,name'
    _table = 'gnuhealth_imaging_test_type'

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)


class ImagingTest(models.Model, ):
    'Imaging Test'
    _name = 'gnuhealth.imaging.test'
    _description = 'Imaging Test'
    _order = 'id,name'
    _table = 'gnuhealth_imaging_test'

    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
    test_type = fields.Many2one(
        'gnuhealth.imaging.test.type', 'Type',
        required=True)
    product = fields.Many2one('product.product', 'Service', required=True)
    active = fields.Boolean('Active', select=True,default=True)



class ImagingTestRequest(models.Model ):
    'Imaging Test Request'
    _name = 'gnuhealth.imaging.test.request'
    _description = 'Imaging Test Request'
    _order = 'date desc,request desc'
    _table = 'gnuhealth_imaging_test_request'

    patient = fields.Many2one('gnuhealth.patient', 'Patient', required=True)
    date = fields.Datetime('Date', required=True,default=datetime.date.today())
    requested_test = fields.Many2one(
        'gnuhealth.imaging.test', 'Test',
        required=True)
    doctor = fields.Many2one('gnuhealth.healthprofessional', 'Doctor', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('done', 'Done'),
    ], 'State', readonly=True,default='draft')
    comment = fields.Text('Comment')
    request = fields.Char('Request', readonly=True)
    urgent = fields.Boolean('Urgent')

    # self._buttons.update({
    #     'requested': {'invisible': ~Eval('state').in_(['draft']),},
    #     'generate_results': { 'invisible': ~Eval('state').in_(['requested'])  }
    #     })

    @classmethod
    def create(self, vlist):
        Sequence = self.env.get('ir.sequence')
        Config = self.env.get('gnuhealth.sequences')
        vlist = [x.copy() for x in vlist]
        for values in vlist:
            if not values.get('request'):
                config = Config(1)
                values['request'] = Sequence.get_id(
                    config.imaging_request_sequence.id)
        return super(ImagingTestRequest).create(vlist)

    @classmethod
    def copy(self, tests, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['request'] = None
        default['date'] = datetime.date.today()
        return super(ImagingTestRequest, self).copy(tests, default=default)

    @classmethod
    #@.button
    #@Workflow.transition('requested')
    def requested(self, requests):
        pass

    @classmethod
    #open ('health_imaging.wizard_generate_result')
    def generate_results(self, requests):
        pass

    @classmethod
    #@Workflow.transition('done')
    def done(self, requests):
        pass


class ImagingTestResult(models.Model):
    'Imaging Test Result'
    _name = 'gnuhealth.imaging.test.result'
    _description = 'Imaging Test Result'
    _order = 'date desc'
    _table = 'gnuhealth_imaging_test_result'

    patient = fields.Many2one('gnuhealth.patient', 'Patient', readonly=True)
    number = fields.Char('Number', readonly=True)
    date = fields.Datetime('Date', required=True)
    request_date = fields.Datetime('Requested Date', readonly=True)
    requested_test = fields.Many2one(
        'gnuhealth.imaging.test', 'Test',
        required=True)
    request = fields.Many2one(
        'gnuhealth.imaging.test.request', 'Request',
        readonly=True)
    doctor = fields.Many2one('gnuhealth.healthprofessional', 'Doctor',
                             required=True)
    comment = fields.Text('Comment')
    images = fields.One2many ('ir.attachment', 'resource', 'Images')

    _sql_constraints = [
        ('number_uniq',
         'UNIQUE (number)',
         'The test ID code must be unique!')]

    @classmethod
    def create(self, vlist):
        Sequence = self.env.get('ir.sequence')
        Config = self.env.get('gnuhealth.sequences')

        vlist = [x.copy() for x in vlist]
        for values in vlist:
            if not values.get('name'):
                config = Config(1)
                values['number'] = Sequence.get_id(
                    config.imaging_sequence.id)

        return super(ImagingTestResult, self).create(vlist)

    @classmethod
    def search_rec_name(self, name, clause):
        if clause[1].startswith('!') or clause[1].startswith('not '):
            bool_op = 'AND'
        else:
            bool_op = 'OR'
        return [bool_op,
                ('patient',) + tuple(clause[1:]),
                ('number',) + tuple(clause[1:]),
                ]


