from classifier import IntentClassifier
from retriever import HistoricalRetriever
from escalation import escalation_gate

class AppleSupportAgent:
    def __init__(self, golden_path, corpus_path):
        self.classifier=IntentClassifier().fit(golden_path)
        self.retriever=HistoricalRetriever(corpus_path)
    def respond(self, message, k=3):
        intent=self.classifier.predict(message)
        hits=self.retriever.search(message,k=k)
        top=float(hits[0]['similarity']) if hits else 0.0
        escalate,reason=escalation_gate(message,intent,top)
        if escalate:
            reply='Thanks for flagging this. This needs a closer look by Apple Support. Please continue with a support specialist so they can review the issue safely.'
        else:
            best=str(hits[0].get('support_text','')).strip() if hits else ''
            reply=best if best else 'Thanks for reaching out. Please continue with Apple Support so we can take a closer look.'
        return {'intent':intent,'escalate':escalate,'reason':reason,'reply':reply,'evidence':hits}
