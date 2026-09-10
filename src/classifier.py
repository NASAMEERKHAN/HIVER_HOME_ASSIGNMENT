"""Lightweight intent classifier with no compiled ML dependencies.
Uses TF-IDF-style prototype similarity over the hand-labelled golden set.
"""
import csv, math, re
from collections import Counter, defaultdict

TOKEN_RE = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")

class IntentClassifier:
    def __init__(self):
        self.docs=[]; self.labels=[]; self.idf={}; self.vectors=[]

    def _tokens(self, text):
        return TOKEN_RE.findall(str(text).lower())

    def _features(self, text):
        t=self._tokens(text)
        return t + [f"{t[i]} {t[i+1]}" for i in range(len(t)-1)]

    def fit(self, csv_path):
        rows=[]
        with open(csv_path, encoding='utf-8-sig', newline='') as f:
            for r in csv.DictReader(f):
                text=str(r.get('text','')).strip(); label=str(r.get('intent_label','')).strip()
                if text and label: rows.append((text,label))
        self.docs=rows
        df=Counter()
        raw=[]
        for text,label in rows:
            feats=Counter(self._features(text)); raw.append((feats,label)); df.update(feats.keys())
        n=max(1,len(rows)); self.idf={k:math.log((1+n)/(1+v))+1 for k,v in df.items()}
        self.vectors=[]
        for feats,label in raw:
            v={k:c*self.idf.get(k,1.0) for k,c in feats.items()}; norm=math.sqrt(sum(x*x for x in v.values())) or 1
            self.vectors.append(({k:x/norm for k,x in v.items()},label))
        return self

    def predict(self, text):
        q=Counter(self._features(text)); q={k:c*self.idf.get(k,1.0) for k,c in q.items()}; qn=math.sqrt(sum(x*x for x in q.values())) or 1
        q={k:x/qn for k,x in q.items()}
        scores=defaultdict(float)
        for v,label in self.vectors:
            s=sum(q.get(k,0)*x for k,x in v.items()); scores[label]+=max(0,s)
        if not scores: return 'other_unknown'
        return max(scores, key=scores.get)
