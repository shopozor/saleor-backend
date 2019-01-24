from behave import register_type
import parse


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
    SECONDS_IN_ONE_SECOND = 1
    SECONDS_IN_ONE_MINUTE = 60
    SECONDS_IN_ONE_HOUR = SECONDS_IN_ONE_MINUTE * 60
    SECONDS_IN_ONE_DAY = SECONDS_IN_ONE_HOUR * 24
    SECONDS_IN_ONE_WEEK = SECONDS_IN_ONE_DAY * 7
    SECONDS_IN_ONE_MONTH = SECONDS_IN_ONE_DAY * 30
    SECONDS_IN_ONE_YEAR = SECONDS_IN_ONE_DAY * 360
    switch = {
        'secondes': SECONDS_IN_ONE_SECOND,
        'seconde': SECONDS_IN_ONE_SECOND,
        'minutes': SECONDS_IN_ONE_MINUTE,
        'minute': SECONDS_IN_ONE_MINUTE,
        'heures': SECONDS_IN_ONE_HOUR,
        'heure': SECONDS_IN_ONE_HOUR,
        'jours': SECONDS_IN_ONE_DAY,
        'jour': SECONDS_IN_ONE_DAY,
        'semaines': SECONDS_IN_ONE_WEEK,
        'semaine': SECONDS_IN_ONE_WEEK,
        'mois': SECONDS_IN_ONE_MONTH,
        'ans': SECONDS_IN_ONE_YEAR,
        'an': SECONDS_IN_ONE_YEAR
    }
    return switch[unit]


@parse.with_pattern(r'secondes?|minutes?|heures?|jours?|semaines?|mois|ans?')
def parse_duration_unit(unit):
    return unit_to_seconds(unit)


register_type(DurationInSecondsType=parse_duration_unit)
