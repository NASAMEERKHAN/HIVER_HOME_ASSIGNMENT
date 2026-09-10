"""Lightweight historical retriever; avoids scikit-learn/SciPy DLLs."""
import csv, math, re
from collections import Counter
TOKEN_RE=re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")

class HistoricalRetriever:
    def __init__(self, corpus_path, max_features=60000):
        self.rows=[]; df=Counter()
        with open(corpus_path, encoding='utf-8-sig', newline='') as f:
            for r in csv.DictReader(f):
                text=str(r.get('customer_text','')).strip()
                if not text: continue
                feats=self._features(text); df.update(set(feats)); self.rows.append((r,Counter(feats)))
        n=max(1,len(self.rows)); self.idf={k:math.log((1+n)/(1+c))+1 for k,c in df.most_common(max_features)}
        self.vectors=[]
        for r,c in self.rows:
            v={k:x*self.idf[k] for k,x in c.items() if k in self.idf}; norm=math.sqrt(sum(x*x for x in v.values())) or 1
            self.vectors.append((r,{k:x/norm for k,x in v.items()}))

    def _features(self,text):
        t=TOKEN_RE.findall(str(text).lower()); return t+[f'{t[i]} {t[i+1]}' for i in range(len(t)-1)]

    def search(self, query, k=5, exclude_customer_ids=None):
        q=Counter(self._features(query)); q={x:c*self.idf.get(x,1) for x,c in q.items() if x in self.idf}; norm=math.sqrt(sum(x*x for x in q.values())) or 1; q={x:xv/norm for x,xv in q.items()}
        excluded=set(map(str,exclude_customer_ids or [])); scored=[]
        for r,v in self.vectors:
            if str(r.get('customer_tweet_id','')) in excluded: continue
            s=sum(q.get(x,0)*y for x,y in v.items()); scored.append((s,r))
        scored.sort(key=lambda z:z[0], reverse=True)
        out=[]
        for s,r in scored[:k]:
            d=dict(r); d['similarity']=s; out.append(d)
        return out
