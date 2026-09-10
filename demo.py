import sys
sys.path.insert(0,'src')
from agent import AppleSupportAgent
agent=AppleSupportAgent('data/apple_golden_set.csv','data/apple_support_pairs.csv')
message='My iPhone battery is draining very fast after the latest update.'
r=agent.respond(message)
print('INTENT:',r['intent']); print('ESCALATE:',r['escalate']); print('REASON:',r['reason']); print('REPLY:',r['reply'])
print('\nEVIDENCE:')
for e in r['evidence']:
    print(f"[{e['similarity']:.3f}] CUSTOMER: {e.get('customer_text','')}\n    SUPPORT: {e.get('support_text','')}")
