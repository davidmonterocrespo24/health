Odoo Medical
============

This module is an update for Odoo 13 of the modules in
* https://github.com/OCA/partner-contact

Check the ``__manifest__.py`` for the specific dependencies.

Usage
=====

Patients
--------

Patients are available in the ``Medical`` App, in the ``Patients`` submenu.

Medical Abstract Entity
-----------------------

The Medical Abstract Entity (``medical.abstract.entity``) is an AbstractModel
that provides for a central base that all medical entities should inherit from.

A Medical Entity is any partner that also requires a medical context. Examples:

* MedicalCenter
* MedicalPatient
* MedicalPhysician
* MedicalPharmacy

Some base views are also provided in order to make it easy to create new medical
entities & maintain uniformity between them:

* Kanban - ``medical_asbsract_entity_view_kanban``
* Tree - ``medical_asbsract_entity_view_tree``
* Form - ``medical_asbsract_entity_view_form``
* Search - ``medical_asbsract_entity_view_search``

When inheriting these views, you must define the inheritance mode as ``primary``,
such as in the following example:

    <record id="medical_patient_view_tree" model="ir.ui.view">
        <field name="name">medical.patient.tree</field>
        <field name="model">medical.patient</field>
        <field name="inherit_id" ref="medical_abstract_entity_view_tree" />
        <field name="mode">primary</field>
        <field name="arch" type="xml">
            <xpath expr="//tree" position="attributes">
                <attribute name="string">Patients</attribute>
            </xpath>
            <xpath expr="//field[@name='email']" position="after">
                <field name="identification_code" />
                <field name="age" />
                <field name="gender" />
            </xpath>
        </field>
    </record>

Take a look at ``medical/views/medical_patient.xml``, or any of the other medical
entity views for more examples.

Credits
=======

This version
------------
* Ángel Ramírez Isea <angel.ramirez.isea@yandex.com>

GNU Health creator
------------------
* Dr. Luis Falcón, MD <falcon@gnuhealth.org>

``medical`` Original Contributors
---------------------------------
* Dave Lasley <dave@laslabs.com>
* Jonathan Nemry <jonathan.nemry@acsone.eu>
* Brett Wood <bwood@laslabs.com>
* Jordi Ballester Alomar <jordi.ballester@eficent.com>

The current project as it is today represents an evolution of the original work
started by Luis Falcon. See https://sourceforge.net/projects/medical/files/Oldfiles/1.0.1,
that later became GNU Health (see
http://health.gnu.org/). The original code was licensed under GPL.

On Nov 27, 2012 derivative code was published in https://github.com/OCA/vertical-medical,
by Tech-Receptives Solutions Pvt. Ltd., licensed
under AGPL.  The license change was unauthorized by the original
author. See https://github.com/OCA/vertical-medical/commit/f0a664749edaea36f6749c34bfb04f1fc4cc9ea4

On Feb 17, 2017 the branch 9.0 of the project was relicensed to LGPL.
https://github.com/OCA/vertical-medical/pull/166. Various prior contributors
approved the relicense, but not all.

On Jan 25, 2018, GNU Health claimed that the original code and attribution
should be respected, and after further investigation the Odoo Community
Association Board agreed to switch the license back to GPL v3 to respect the
rights of the original author.

Although no trace of relationship was found between the code at the date
and the original code from 2012, through the commit history of the project one
can see that the current status of the project is the end result of an
evolutionary process. The Odoo Community Association Board concluded that
the original license should be respected for ethical reasons.

More information can be read here - https://odoo-community.org/blog/our-blog-1/post/vertical-medical-75.

Maintainer
----------

This module is maintained by Asociaciones Cooperativas  de
Procesamiento Unificado Informático, R.S.; Simón Rodríguez para
el Conocimiento Libre, R.S.; y Soluciones Informáticas para el
Desarrollo de Inclusión Social, R.S.

To contribute to this module, please visit https://labviv.org.ve.
