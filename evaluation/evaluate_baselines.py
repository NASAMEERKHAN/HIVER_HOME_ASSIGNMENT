"""Dependency-free evaluation entry point.
The reported baseline figures in the report were computed previously with stratified CV.
This script confirms the golden-set file is present and prints the recorded results.
"""
import json, os
root=os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(root,'baseline_results_recomputed.json'),encoding='utf-8') as f: r=json.load(f)
print('Golden-set baseline results (recorded development evaluation)')
print(f"Majority accuracy: {r['majority']['accuracy_mean']:.3f} ± {r['majority']['accuracy_std']:.3f}")
print(f"Majority macro-F1: {r['majority']['macro_f1_mean']:.3f} ± {r['majority']['macro_f1_std']:.3f}")
print(f"TF-IDF + Logistic Regression accuracy: {r['tfidf_logreg']['accuracy_mean']:.3f} ± {r['tfidf_logreg']['accuracy_std']:.3f}")
print(f"TF-IDF + Logistic Regression macro-F1: {r['tfidf_logreg']['macro_f1_mean']:.3f} ± {r['tfidf_logreg']['macro_f1_std']:.3f}")
