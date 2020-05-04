from yargy import Parser, rule, and_, not_, or_
from yargy.interpretation import fact
from yargy.predicates import gram
from yargy.relations import gnc_relation
from yargy.pipelines import morph_pipeline

import pymorphy2

morph = pymorphy2.MorphAnalyzer()

LimbState = fact(
    'LimbState',
    ['state'],
)
 
Limb = fact(
    'limb',
    ['name'],
)

Disease = fact(
    'Person',
    ['limb', 'limbstate']
)

LIMBSTATE = rule(
    gram('VERB').interpretation(
        LimbState.state
    )
).interpretation(
    LimbState
)

LIMB = rule(
    gram('NOUN').interpretation(
        Limb.name
    )
).interpretation(
    Limb
)

DISEASE = or_(
    rule(LIMB.interpretation(
        Disease.limb
    ), LIMBSTATE.interpretation(
        Disease.limbstate
    )),
    rule(LIMBSTATE.interpretation(
        Disease.limbstate
    ),LIMB.interpretation(
        Disease.limb
    )),
).interpretation(
    Disease
)

parser = Parser(DISEASE)

LIMB_SCORE = {
    'сердце': 0.8,
    'голова': 0.7,
    'колено': 0.3
}

LIMB_STATE_SCORE = {
    'прострелить': 0.8,
}

# возвращает карту вида ключевое слово - его критический "счет"
def analyze(str):
    scores = {}
    for match in parser.findall(str):
        limb = match.fact.limb.name
        parsed = morph.parse(limb)
        normalized = parsed[0].normal_form
        limb_score = 0.2
        if normalized in LIMB_SCORE:
            limb_score = LIMB_SCORE[normalized]
        scores[limb] = limb_score
        
        limb_state = match.fact.limbstate.state
        parsed = morph.parse(limb_state)
        normalized = parsed[0].normal_form
        limbstate_score = 0.2
        if normalized in LIMB_STATE_SCORE:
            limbstate_score = LIMB_STATE_SCORE[normalized]
        scores[limb_state] = limbstate_score
    return scores
