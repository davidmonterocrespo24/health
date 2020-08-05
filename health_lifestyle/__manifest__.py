# Copyright 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright 2020 LabViv
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Health Lifestyle',
    'summary': 'Registros de estilo de vida.',
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'depends': [
        'medical',
    ],
    'Author': 'LabViv',
    'website': "https://www.labviv.org.ve",
    'description': """
        - Evaluación del Estilo de Vida de las personas.
        - Recopila información sobre hábitos y la sexualidad del paciente.
        - Hábitos alimenticios y dietas.
        - Patrones de sueño.
        - Base de datos de drogas recreativas de NIDA.
        - Clasificaciones de drogas Henningfield.
        - Adicciones a las drogas / alcohol.
        - Actividad física (entrenamiento / ejercicio).
        - Sexualidad y comportamiento sexual.
        - Conducción, seguridad en el hogar y niños.
    """,
    'license': 'GPL-3',
    'data': [
        'security/access_rights.xml',
        'security/ir.model.access.csv',
        'data/recreational_drugs.xml',
        'data/vegetarian_types.xml',
        'data/diets_beliefs.xml',
        'views/drugs_recreational.xml',
        'views/diets_beliefs.xml',
        'views/gnuhealth_patient_cage_tree.xml',
        'views/gnuhealth_patient_cage.xml',
        'views/gnuhealth_patient.xml',
        'views/gnuhealth_recreational_drugs_tree.xml',
        'views/gnuhealth_recreational_drugs.xml',
        'views/gnuhealth_vegetarian_types_form.xml',
        'views/gnuhealth_vegetarian_types_tree.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'maintainer': 'Kaylenis Mardach <kaykmm@yandex.com>'
}
