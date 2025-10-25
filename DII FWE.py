import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
from sklearn.impute import SimpleImputer
from dadapy.feature_weighting import FeatureWeighting
import matplotlib.pyplot as plt

# Read file
def read_data(file_path):
    df = pd.read_excel(file_path)
    y = df.iloc[:, 0].values.astype(float)  
    X = df.iloc[:, 1:12].values.astype(float)  
    feature_names = df.columns[1:12].tolist()  
    return X, y, feature_names


def preprocess_data(X, y):
    imputer = SimpleImputer(strategy="median")
    X_imputed = imputer.fit_transform(X)
    y_imputed = imputer.fit_transform(y.reshape(-1, 1)).ravel()  

    # Normalization
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)
    
    return X_scaled, y_imputed

# ground truth
def build_ground_truth(X, y, supervised=True):
    if supervised:
        return y.reshape(-1, 1)  
    else:
        return X  

# DII feature selection and weighting function - L1 regularization
def run_dii(X, y, l1_grid, max_epochs=120, n_splits=5, supervised=True):
    best_results = []
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    # Cross-validation
    for train_idx, val_idx in kf.split(X):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]
        
        
        XB_train = build_ground_truth(X_train, y_train, supervised)
        XB_val = build_ground_truth(X_val, y_val, supervised)

        fw = FeatureWeighting(XA=X_train, XB=XB_train, metric_A="euclidean", metric_B="euclidean")
        
        best_l1 = None
        best_dii = np.inf
        best_weights = None
        best_nnz = 0

        for l1 in l1_grid:
            res = fw.return_weights_optimize_dii(l1=l1, nepochs=max_epochs)
            dii = res.get("dii", None)
            weights = res.get("weights", None)
            nnz = np.sum(weights > 0)

            if dii < best_dii:
                best_l1 = l1
                best_dii = dii
                best_weights = weights
                best_nnz = nnz

        # Store the best results
        best_results.append({
            "fold_dii": best_dii,
            "l1": best_l1,
            "weights": best_weights,
            "nnz": best_nnz
        })

    # Aggregate results
    weights_stack = np.vstack([res["weights"] for res in best_results])
    feature_weights = np.mean(weights_stack, axis=0)  
    return feature_weights, best_results

# Greedy reverse elimination
def run_dii_backward_greedy(X, y, max_epochs=120, n_splits=5, supervised=True):
    best_results = []
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    for train_idx, val_idx in kf.split(X):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]
        
        XB_train = build_ground_truth(X_train, y_train, supervised)
        XB_val = build_ground_truth(X_val, y_val, supervised)

        fw = FeatureWeighting(XA=X_train, XB=XB_train, metric_A="euclidean", metric_B="euclidean")

        active_features = np.arange(X_train.shape[1])  ## Feature Index
        best_weights = None
        best_dii = np.inf
        best_nnz = 0

        while len(active_features) > 1:
            # DII optimization
            res = fw.return_weights_optimize_dii(l1=0.0, nepochs=max_epochs)
            weights = res.get("weights", None)
            dii = res.get("dii", None)
            nnz = np.sum(weights > 0)

            if dii < best_dii:
                best_dii = dii
                best_weights = weights
                best_nnz = nnz

            min_weight_index = np.argmin(np.abs(weights[active_features]))
            active_features = np.delete(active_features, min_weight_index)

        best_results.append({
            "fold_dii": best_dii,
            "weights": best_weights,
            "nnz": best_nnz
        })

    weights_stack = np.vstack([res["weights"] for res in best_results])
    feature_weights = np.mean(weights_stack, axis=0)  
    return feature_weights, best_results


def export_feature_weights(feature_weights, feature_names, method_name):
    # 输出每个特征的权重
    print(f"\n=== {method_name} Feature weight ===")
    for feature, weight in zip(feature_names, feature_weights):
        print(f"{feature}: {weight:.6f}")
    
    # 导出到CSV
    result_df = pd.DataFrame({
        "Feature": feature_names,
        "Weight": feature_weights
    })
    result_df = result_df.sort_values(by="Weight", ascending=False, key=np.abs).reset_index(drop=True)
    result_df.to_csv(f"{method_name}_feature_weights.csv", index=False)
    print(f"\n{method_name} '{method_name}_feature_weights.csv'")

# 可视化特征权重
def plot_feature_weights(feature_weights, feature_names, method_name):
    plt.figure(figsize=(10, 6))
    plt.barh(feature_names, feature_weights, color='skyblue')
    plt.xlabel('Feature Weight')
    plt.title(f'{method_name} - Feature Weights')
    plt.tight_layout()
    plt.savefig(f"{method_name}_feature_weights.png")
    plt.show()


def main():
    file_path = "Co_data.xlsx"  
    X, y, feature_names = read_data(file_path)  
    X_scaled, y_scaled = preprocess_data(X, y)  

    # Different intensities of L1 regularization
    l1_grid = [0.0, 1e-6, 5e-6, 1e-5, 5e-5, 1e-4, 5e-4, 1e-3]


    feature_weights_l1, best_results_l1 = run_dii(X_scaled, y_scaled, l1_grid, max_epochs=120, n_splits=5, supervised=True)
    export_feature_weights(feature_weights_l1, feature_names, "L1 regularization")
    plot_feature_weights(feature_weights_l1, feature_names, "L1 regularization")


    feature_weights_greedy, best_results_greedy = run_dii_backward_greedy(X_scaled, y_scaled, max_epochs=120, n_splits=5, supervised=True)
    export_feature_weights(feature_weights_greedy, feature_names, "backward greedy")
    plot_feature_weights(feature_weights_greedy, feature_names, "backward greedy")

if __name__ == "__main__":
    main()
