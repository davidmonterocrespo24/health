# -*- coding: utf-8 -*-
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2020 Luis Falcon <lfalcon@gnuhealth.org>
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
from Datetime import Datetime
from odoo import models, fields, api

__all__ = ['WizardGenerateResult', 'RequestImagingTest',
    'RequestPatientImagingTestStart', 'RequestPatientImagingTest']


class WizardGenerateResult():#hereda de Wizard
    'Generate Results'
    _name = 'wizard.generate.result'
    start_state = 'open_'
    #open_ = StateAction('health_imaging.act_imaging_test_result_view')

    # def do_open_(self, action):
    #     Request = self.env.get('gnuhealth.imaging.test.request')
    #     Result = self.env.get('gnuhealth.imaging.test.result')
    #
    #     request_data = []
    #     requests = Request.browse(Transaction().context.get('active_ids'))
    #     for request in requests:
    #         request_data.append({
    #             'patient': request.patient.id,
    #             'date': Datetime.now(),
    #             'request_date': request.date,
    #             'requested_test': request.requested_test,
    #             'request': request.id,
    #             'doctor': request.doctor})
    #     results = Result.create(request_data)
    #
    #     action['pyson_domain'] = PYSONEncoder().encode(
    #         [('id', 'in', [r.id for r in results])])
    #
    #     Request.requested(requests)
    #     Request.done(requests)
    #     return action, {}


class RequestImagingTest(models.TransientModel):
    'Request - Test'
    _name = 'gnuhealth.request-imaging-test'
    _table = 'gnuhealth_request_imaging_test'

    request = fields.Many2one('gnuhealth.patient.imaging.test.request.start',
        'Request', required=True)
    test = fields.Many2one('gnuhealth.imaging.test', 'Test', required=True)


class RequestPatientImagingTestStart(models.TransientModel):
    'Request Patient Imaging Test Start'
    _name = 'gnuhealth.patient.imaging.test.request.start'

    date = fields.Datetime('Date',default=Datetime.now())
    patient = fields.Many2one('gnuhealth.patient', 'Patient', required=True)
    doctor = fields.Many2one('gnuhealth.healthprofessional', 'Doctor',
        required=True, help="Doctor who Request the lab tests.")
    tests = fields.Many2Many('gnuhealth.request-imaging-test', 'request',
        'test', 'Tests', required=True)
    urgent = fields.Boolean('Urgent')

    def default_doctor(self):
        HealthProf= self.env.get('gnuhealth.healthprofessional')
        hp = HealthProf.get_health_professional()
        if not hp:
            RequestPatientImagingTestStart.raise_user_error(
                "No health professional associated to this user !")
        return hp


class RequestPatientImagingTest():#hereda de wizard
    'Request Patient Imaging Test'
    _name = 'gnuhealth.patient.imaging.test.request'

    # start = StateView('gnuhealth.patient.imaging.test.request.start',
    #     'health_imaging.patient_imaging_test_request_start_view_form', [
    #         Button('Cancel', 'end', 'tryton-cancel'),
    #         Button('Request', 'request', 'tryton-ok', default=True),
    #         ])
    # request = StateTransition()

    def transition_request(self):
        ImagingTestRequest = self.env.get('gnuhealth.imaging.test.request')
        Sequence = self.env.get('ir.sequence')
        Config = self.env.get('gnuhealth.sequences')

        config = Config(1)
        request_number = Sequence.get_id(config.imaging_request_sequence.id)
        imaging_tests = []
        for test in self.start.tests:
            imaging_test = {}
            imaging_test['request'] = request_number
            imaging_test['requested_test'] = test.id
            imaging_test['patient'] = self.start.patient.id
            if self.start.doctor:
                imaging_test['doctor'] = self.start.doctor.id
            imaging_test['date'] = self.start.date
            imaging_test['urgent'] = self.start.urgent
            imaging_tests.append(imaging_test)
        ImagingTestRequest.create(imaging_tests)

        return 'end'
