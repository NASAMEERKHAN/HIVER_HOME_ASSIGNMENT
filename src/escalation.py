HIGH_RISK = ['fraud','fraudulent','unauthorized','stolen','scam','shock','electric','overheating','burn','smoke']
SEVERE = ['keeps restarting','keeps freezing',"won't turn on","doesn't turn on",'touchscreen','very hot','battery draining','account disabled','cannot access','can\'t access']

def escalation_gate(text, intent, top_similarity=0.0):
    t=(text or '').lower()
    if any(x in t for x in HIGH_RISK): return True,'Potential safety, fraud, or security issue.'
    if any(x in t for x in SEVERE): return True,'Severe or persistent device/account issue.'
    if intent=='account_access_security': return True,'Account, authentication, activation, or security issue.'
    if top_similarity < 0.08: return True,'Insufficiently similar historical evidence to safely ground a response.'
    return False,'Sufficient historical evidence and no high-risk trigger.'
