from sklearn.ensemble import RandomForestClassifier


def get_model():
    model = RandomForestClassifier(n_estimators=5, max_depth=15, criterion='gini', min_samples_leaf=1, verbose=1)
    return model
