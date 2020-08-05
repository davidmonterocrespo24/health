# Copyright 2008-2020 Luis Falcon.
# Copyright 2011-2020 GNU Solidario.
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo.tests.common import TransactionCase


class TestHealthLifestyle(TransactionCase):
    def setUp(self,):
        super(TestHealthLifestyle, self).setUp()
        self.model_obj = self.env['health.lifesyle']
        self.vals = {'name': 'Test Health Lifestyle'}
