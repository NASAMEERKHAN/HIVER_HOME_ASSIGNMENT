"""LLM-as-judge harness. Requires OPENAI_API_KEY and an API-compatible client setup.
This file intentionally does not fabricate judge scores or human agreement.
"""
import json, os
RUBRIC={
 'groundedness':'Is every factual troubleshooting claim supported by the retrieved historical evidence?',
 'relevance':'Does the reply directly address the customer intent?',
 'helpfulness':'Would this move the customer toward resolution?',
 'safety':'Does it avoid risky unsupported instructions and escalate when appropriate?',
 'style':'Is it concise, empathetic, and appropriate for support?'
}
def rubric_text():
    return '\n'.join(f'- {k}: {v}' for k,v in RUBRIC.items())

def build_prompt(customer, reply, evidence):
    ev='\n'.join(f"Customer: {x['customer_text']}\nSupport: {x['support_text']}" for x in evidence)
    return f'''Score the following support reply from 1-5 on each dimension. Return JSON only with numeric scores and one short reason per dimension.\n\nRubric:\n{rubric_text()}\n\nCustomer: {customer}\nReply: {reply}\nHistorical evidence:\n{ev}'''

if __name__=='__main__':
    print('LLM judge harness ready. Set your provider/API key and add a small labeled sample before producing judge metrics.')
