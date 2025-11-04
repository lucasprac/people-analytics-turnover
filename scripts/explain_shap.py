"""
Gera gráficos SHAP e explicabilidade global e individual
"""
import pandas as pd
import shap
import joblib
import matplotlib.pyplot as plt
import os


def main():
    model = joblib.load('models/turnover_rf_model.pkl')
    feat_names = joblib.load('models/feature_names.pkl')
    # Exemplo: usar um subconjunto sintético a partir dos nomes de features
    import numpy as np
    X_sample = pd.DataFrame(np.random.normal(0, 1, size=(100, len(feat_names))), columns=feat_names)

    explainer = shap.TreeExplainer(model)
    sv = explainer.shap_values(X_sample)
    sv1 = sv[1] if isinstance(sv, list) else sv

    os.makedirs('docs', exist_ok=True)
    plt.figure(figsize=(10,8))
    shap.summary_plot(sv1, X_sample, plot_type='bar', show=False)
    plt.savefig('docs/shap_summary_bar.png', dpi=200, bbox_inches='tight')

    plt.figure(figsize=(12,8))
    shap.summary_plot(sv1, X_sample, show=False)
    plt.savefig('docs/shap_summary_beeswarm.png', dpi=200, bbox_inches='tight')

    print('Saved SHAP plots in docs/')


if __name__ == '__main__':
    main()
