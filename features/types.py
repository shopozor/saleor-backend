from behave import register_type
import parse
from datetime import timedelta


@parse.with_pattern(r'client|administrateur')
def parse_user_type(text):
    return text


register_type(UserType=parse_user_type)


@parse.with_pattern(r'Consommateur|Producteur|Responsable|Rex|Softozor')
def parse_persona_type(text):
    return text


register_type(PersonaType=parse_persona_type)


@parse.with_pattern(r'valides|invalides')
def parse_user_credentials_validity(validity):
    return validity == 'valides'


register_type(ValidityType=parse_user_credentials_validity)


def unit_to_seconds(unit):
    switch = {
        'secondes': 1,
        'seconde': 1,
        'minutes': timedelta(minutes=1).seconds(),
        'minute': timedelta(minutes=1).seconds(),
        'heures': timedelta(hours=1).seconds(),
        'heure': timedelta(hours=1).seconds(),
        'jours': timedelta(days=1).seconds(),
        'jour': timedelta(days=1).seconds(),
        'semaines': timedelta(weeks=1).seconds(),
        'semaine': timedelta(weeks=1).seconds(),
        'mois': timedelta(days=30).seconds(),
        'ans': timedelta(days=360).seconds(),
        'an': timedelta(days=360).seconds()
    }
    return switch[unit]


@parse.with_pattern(r'secondes?|minutes?|heures?|jours?|semaines?|mois|ans?')
def parse_duration_unit(unit):
    return unit_to_seconds(unit)


register_type(DurationInSecondsType=parse_duration_unit)
