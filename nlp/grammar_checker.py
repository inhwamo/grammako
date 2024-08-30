def check_sov_order(pos_tagged):
    has_subject = any(tag in ['NP', 'NNG', 'NNP'] for _, tag in pos_tagged) # Pronoun, Common Noun, Proper Noun
    has_object = any(tag == 'JKO' for _, tag in pos_tagged) # Object Case Particle: 을·를
    has_verb = any(tag.startswith('V') for _, tag in pos_tagged)
    
    if not has_subject and has_verb:
        return "Sentence may be missing a subject."
    if has_object and not has_verb:
        return "Sentence has an object but may be missing a verb."
    return None

def check_sentence_completeness(pos_tagged):
    if not any(tag.startswith('V') for _, tag in pos_tagged):
        return "Sentence may be incomplete (missing a verb)." # Doesn't work with imperative sentences
    return None

def check_proper_ending(pos_tagged): # sentence ends with ending POS or .?! e.g. "습니다"
    if pos_tagged[-1][1] not in ['EF', 'EC','EP','SF']: 
        return "Sentence may be missing a proper ending." 
    return None 

def check_case_particles(pos_tagged):
    subject_particle = any(tag in ['JKS', 'JX'] for _, tag in pos_tagged) # JKS = 이/가, JX = 은/는/도
    object_particle = any(tag == 'JKO' for _, tag in pos_tagged) # 을·를
    
    if not subject_particle and not object_particle:
        return "Sentence may be missing case particles."
    return None

def check_honorific_consistency(pos_tagged):
    honorific_subject = any(word in ['저', '제'] for word, _ in pos_tagged)
    honorific_verb = any(tag == 'EP' for _, tag in pos_tagged) # EP = 았/었/
    
    if honorific_subject and not honorific_verb:
        return "Inconsistent use of honorifics. Consider using an honorific verb ending."
    return None

## TODO: more honorific checks

def check_grammar(pos_tagged):
    issues = []
    checks = [
        check_sov_order,
        check_sentence_completeness,
        check_proper_ending,
        check_case_particles,
        check_honorific_consistency
    ]

    for check in checks:
        issue = check(pos_tagged)
        if issue:
            issues.append(issue)

    return issues