"""
Online Order Delivery Time Prediction System
Predicts delivery time using logistics and traffic data with machine learning
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

def generate_delivery_dataset(n_samples=1000, random_state=42):
    """Generate synthetic delivery dataset with logistics and traffic features"""
    np.random.seed(random_state)
    
    data = {
        'Order_ID': [f'ORD{i:06d}' for i in range(n_samples)],
        'Delivery_Distance_km': np.random.uniform(1, 50, n_samples),
        'Traffic_Density_percent': np.random.uniform(10, 100, n_samples),
        'Weather_Condition': np.random.choice(['Clear', 'Rainy', 'Foggy', 'Snowy'], n_samples),
        'Order_Priority': np.random.choice(['Standard', 'Express', 'Premium'], n_samples),
        'Order_Volume_items': np.random.randint(1, 20, n_samples),
        'Delivery_Partner_Experience_years': np.random.uniform(0.5, 10, n_samples),
        'Time_of_Day': np.random.choice(['Morning', 'Afternoon', 'Evening', 'Night'], n_samples),
        'Day_of_Week': np.random.randint(1, 8, n_samples),
        'Number_of_Stops': np.random.randint(1, 15, n_samples),
        'Vehicle_Type': np.random.choice(['Bike', 'Scooter', 'Car', 'Van'], n_samples),
        'Pickup_Processing_Time_min': np.random.uniform(5, 30, n_samples),
        'Distance_to_Warehouse_km': np.random.uniform(2, 30, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Generate delivery time target (in minutes)
    # Base time calculation
    delivery_time = (df['Delivery_Distance_km'] * 2.5) + \
                   (df['Traffic_Density_percent'] / 10) + \
                   (df['Order_Volume_items'] * 1.5) + \
                   (df['Number_of_Stops'] * 3) + \
                   df['Pickup_Processing_Time_min']
    
    # Add weather impact
    weather_impact = df['Weather_Condition'].map({'Clear': 0, 'Rainy': 5, 'Foggy': 8, 'Snowy': 12})
    delivery_time += weather_impact
    
    # Add priority impact (negative for express)
    priority_impact = df['Order_Priority'].map({'Standard': 0, 'Express': -3, 'Premium': -5})
    delivery_time += priority_impact
    
    # Add experience factor
    delivery_time -= (df['Delivery_Partner_Experience_years'] * 0.5)
    
    # Add time of day impact
    time_impact = df['Time_of_Day'].map({'Morning': 2, 'Afternoon': 5, 'Evening': 3, 'Night': 8})
    delivery_time += time_impact
    
    # Add noise
    delivery_time += np.random.normal(0, 3, n_samples)
    
    # Ensure positive values
    df['Delivery_Time_minutes'] = np.maximum(delivery_time, 10)
    
    return df

def preprocess_data(df):
    """Preprocess the dataset for modeling"""
    df_processed = df.copy()
    
    # Encode categorical variables
    le_weather = LabelEncoder()
    le_priority = LabelEncoder()
    le_time = LabelEncoder()
    le_vehicle = LabelEncoder()
    
    df_processed['Weather_encoded'] = le_weather.fit_transform(df_processed['Weather_Condition'])
    df_processed['Priority_encoded'] = le_priority.fit_transform(df_processed['Order_Priority'])
    df_processed['Time_encoded'] = le_time.fit_transform(df_processed['Time_of_Day'])
    df_processed['Vehicle_encoded'] = le_vehicle.fit_transform(df_processed['Vehicle_Type'])
    
    # Select features for modeling
    feature_cols = [
        'Delivery_Distance_km', 'Traffic_Density_percent', 'Order_Volume_items',
        'Delivery_Partner_Experience_years', 'Number_of_Stops', 'Pickup_Processing_Time_min',
        'Distance_to_Warehouse_km', 'Day_of_Week', 'Weather_encoded', 'Priority_encoded',
        'Time_encoded', 'Vehicle_encoded'
    ]
    
    return df_processed, feature_cols

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple regression models"""
    models = {}
    results = {}
    
    # Model 1: Linear Regression
    print("Training Linear Regression...")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    
    models['Linear Regression'] = lr_model
    results['Linear Regression'] = {
        'predictions': y_pred_lr,
        'mae': mean_absolute_error(y_test, y_pred_lr),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred_lr)),
        'r2': r2_score(y_test, y_pred_lr)
    }
    
    # Model 2: Random Forest Regressor
    print("Training Random Forest Regressor...")
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    
    models['Random Forest'] = rf_model
    results['Random Forest'] = {
        'predictions': y_pred_rf,
        'mae': mean_absolute_error(y_test, y_pred_rf),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred_rf)),
        'r2': r2_score(y_test, y_pred_rf)
    }
    
    # Model 3: Gradient Boosting Regressor
    print("Training Gradient Boosting Regressor...")
    gb_model = GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
    gb_model.fit(X_train, y_train)
    y_pred_gb = gb_model.predict(X_test)
    
    models['Gradient Boosting'] = gb_model
    results['Gradient Boosting'] = {
        'predictions': y_pred_gb,
        'mae': mean_absolute_error(y_test, y_pred_gb),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred_gb)),
        'r2': r2_score(y_test, y_pred_gb)
    }
    
    return models, results

def plot_delivery_distribution(df):
    """Plot distribution of delivery times"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram
    axes[0].hist(df['Delivery_Time_minutes'], bins=30, color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0].axvline(df['Delivery_Time_minutes'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["Delivery_Time_minutes"].mean():.1f}')
    axes[0].axvline(df['Delivery_Time_minutes'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df["Delivery_Time_minutes"].median():.1f}')
    axes[0].set_xlabel('Delivery Time (minutes)', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[0].set_title('Distribution of Delivery Times', fontsize=12, fontweight='bold')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Box plot by priority
    priority_order = ['Standard', 'Express', 'Premium']
    df_sorted = df.copy()
    df_sorted['Order_Priority'] = pd.Categorical(df_sorted['Order_Priority'], categories=priority_order, ordered=True)
    df_sorted = df_sorted.sort_values('Order_Priority')
    
    axes[1].boxplot([df[df['Order_Priority'] == p]['Delivery_Time_minutes'].values for p in priority_order],
                    labels=priority_order, patch_artist=True)
    axes[1].set_ylabel('Delivery Time (minutes)', fontsize=11, fontweight='bold')
    axes[1].set_title('Delivery Time by Order Priority', fontsize=12, fontweight='bold')
    axes[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/delivery_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved: delivery_distribution.png")
    plt.close()

def plot_model_comparison(results, y_test):
    """Compare model performance metrics"""
    models = list(results.keys())
    metrics = ['mae', 'rmse', 'r2']
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    colors = ['#3498db', '#e74c3c', '#f39c12']
    
    for idx, metric in enumerate(metrics):
        values = [results[m][metric] for m in models]
        axes[idx].bar(models, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        axes[idx].set_ylabel(metric.upper(), fontsize=11, fontweight='bold')
        axes[idx].set_title(f'{metric.upper()} Comparison', fontsize=12, fontweight='bold')
        axes[idx].grid(axis='y', alpha=0.3)
        for i, v in enumerate(values):
            axes[idx].text(i, v + max(values)*0.02, f'{v:.4f}', ha='center', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/delivery_model_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: delivery_model_comparison.png")
    plt.close()

def plot_predictions_vs_actual(results, y_test):
    """Plot predicted vs actual delivery times"""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    colors = ['#3498db', '#e74c3c', '#f39c12']
    
    for idx, (model_name, result) in enumerate(results.items()):
        axes[idx].scatter(y_test, result['predictions'], alpha=0.5, s=20, color=colors[idx], edgecolors='black', linewidth=0.5)
        axes[idx].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
        axes[idx].set_xlabel('Actual Time (minutes)', fontsize=11, fontweight='bold')
        axes[idx].set_ylabel('Predicted Time (minutes)', fontsize=11, fontweight='bold')
        axes[idx].set_title(f'{model_name}\nR² = {result["r2"]:.4f}', fontsize=12, fontweight='bold')
        axes[idx].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/delivery_predictions_vs_actual.png', dpi=300, bbox_inches='tight')
    print("Saved: delivery_predictions_vs_actual.png")
    plt.close()

def plot_feature_importance(models, feature_names):
    """Plot feature importance for tree-based models"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Random Forest
    rf_importance = models['Random Forest'].feature_importances_
    rf_indices = np.argsort(rf_importance)[-10:]
    axes[0].barh(range(len(rf_indices)), rf_importance[rf_indices], 
                color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0].set_yticks(range(len(rf_indices)))
    axes[0].set_yticklabels([feature_names[i] for i in rf_indices], fontsize=10)
    axes[0].set_xlabel('Importance', fontsize=11, fontweight='bold')
    axes[0].set_title('Random Forest - Feature Importance', fontsize=12, fontweight='bold')
    axes[0].grid(axis='x', alpha=0.3)
    
    # Gradient Boosting
    gb_importance = models['Gradient Boosting'].feature_importances_
    gb_indices = np.argsort(gb_importance)[-10:]
    axes[1].barh(range(len(gb_indices)), gb_importance[gb_indices], 
                color='#f39c12', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1].set_yticks(range(len(gb_indices)))
    axes[1].set_yticklabels([feature_names[i] for i in gb_indices], fontsize=10)
    axes[1].set_xlabel('Importance', fontsize=11, fontweight='bold')
    axes[1].set_title('Gradient Boosting - Feature Importance', fontsize=12, fontweight='bold')
    axes[1].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/delivery_feature_importance.png', dpi=300, bbox_inches='tight')
    print("Saved: delivery_feature_importance.png")
    plt.close()

def plot_traffic_impact(df):
    """Plot traffic impact on delivery time"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Traffic vs Delivery Time
    axes[0, 0].scatter(df['Traffic_Density_percent'], df['Delivery_Time_minutes'], alpha=0.5, s=30, color='#3498db', edgecolors='black', linewidth=0.5)
    z = np.polyfit(df['Traffic_Density_percent'], df['Delivery_Time_minutes'], 1)
    p = np.poly1d(z)
    axes[0, 0].plot(df['Traffic_Density_percent'].sort_values(), p(df['Traffic_Density_percent'].sort_values()), "r--", linewidth=2)
    axes[0, 0].set_xlabel('Traffic Density (%)', fontsize=11, fontweight='bold')
    axes[0, 0].set_ylabel('Delivery Time (minutes)', fontsize=11, fontweight='bold')
    axes[0, 0].set_title('Traffic Density vs Delivery Time', fontsize=12, fontweight='bold')
    axes[0, 0].grid(alpha=0.3)
    
    # Distance vs Delivery Time
    axes[0, 1].scatter(df['Delivery_Distance_km'], df['Delivery_Time_minutes'], alpha=0.5, s=30, color='#e74c3c', edgecolors='black', linewidth=0.5)
    z = np.polyfit(df['Delivery_Distance_km'], df['Delivery_Time_minutes'], 1)
    p = np.poly1d(z)
    axes[0, 1].plot(df['Delivery_Distance_km'].sort_values(), p(df['Delivery_Distance_km'].sort_values()), "r--", linewidth=2)
    axes[0, 1].set_xlabel('Delivery Distance (km)', fontsize=11, fontweight='bold')
    axes[0, 1].set_ylabel('Delivery Time (minutes)', fontsize=11, fontweight='bold')
    axes[0, 1].set_title('Distance vs Delivery Time', fontsize=12, fontweight='bold')
    axes[0, 1].grid(alpha=0.3)
    
    # Weather impact
    weather_data = df.groupby('Weather_Condition')['Delivery_Time_minutes'].mean().sort_values(ascending=False)
    axes[1, 0].bar(weather_data.index, weather_data.values, color=['#f39c12', '#e74c3c', '#3498db', '#2ecc71'], alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1, 0].set_ylabel('Avg Delivery Time (minutes)', fontsize=11, fontweight='bold')
    axes[1, 0].set_title('Weather Impact on Delivery Time', fontsize=12, fontweight='bold')
    axes[1, 0].grid(axis='y', alpha=0.3)
    for i, v in enumerate(weather_data.values):
        axes[1, 0].text(i, v + 0.5, f'{v:.1f}', ha='center', fontweight='bold')
    
    # Time of day impact
    time_data = df.groupby('Time_of_Day')['Delivery_Time_minutes'].mean().reindex(['Morning', 'Afternoon', 'Evening', 'Night'])
    axes[1, 1].bar(time_data.index, time_data.values, color=['#FFD700', '#FFA500', '#FF6347', '#191970'], alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1, 1].set_ylabel('Avg Delivery Time (minutes)', fontsize=11, fontweight='bold')
    axes[1, 1].set_title('Time of Day Impact on Delivery Time', fontsize=12, fontweight='bold')
    axes[1, 1].grid(axis='y', alpha=0.3)
    for i, v in enumerate(time_data.values):
        axes[1, 1].text(i, v + 0.5, f'{v:.1f}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/delivery_traffic_impact.png', dpi=300, bbox_inches='tight')
    print("Saved: delivery_traffic_impact.png")
    plt.close()

def plot_residuals(results, y_test):
    """Plot residuals for model evaluation"""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    colors = ['#3498db', '#e74c3c', '#f39c12']
    
    for idx, (model_name, result) in enumerate(results.items()):
        residuals = y_test.values - result['predictions']
        axes[idx].scatter(result['predictions'], residuals, alpha=0.5, s=20, color=colors[idx], edgecolors='black', linewidth=0.5)
        axes[idx].axhline(y=0, color='r', linestyle='--', linewidth=2)
        axes[idx].set_xlabel('Predicted Time (minutes)', fontsize=11, fontweight='bold')
        axes[idx].set_ylabel('Residuals (minutes)', fontsize=11, fontweight='bold')
        axes[idx].set_title(f'{model_name}\nMAE = {result["mae"]:.2f} min', fontsize=12, fontweight='bold')
        axes[idx].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/delivery_residuals.png', dpi=300, bbox_inches='tight')
    print("Saved: delivery_residuals.png")
    plt.close()

def main():
    print("="*80)
    print("ONLINE ORDER DELIVERY TIME PREDICTION SYSTEM - MACHINE LEARNING ANALYSIS")
    print("="*80)
    
    # Generate dataset
    print("\n[1] Generating synthetic delivery dataset...")
    df = generate_delivery_dataset(n_samples=1000)
    df.to_csv('/home/ubuntu/delivery_data.csv', index=False)
    print(f"Dataset generated: {df.shape[0]} records")
    print(f"Average delivery time: {df['Delivery_Time_minutes'].mean():.2f} minutes")
    print(f"Min delivery time: {df['Delivery_Time_minutes'].min():.2f} minutes")
    print(f"Max delivery time: {df['Delivery_Time_minutes'].max():.2f} minutes")
    
    # Preprocess data
    print("\n[2] Preprocessing data...")
    df_processed, feature_cols = preprocess_data(df)
    
    # Prepare features and target
    X = df_processed[feature_cols]
    y = df_processed['Delivery_Time_minutes']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"Training set: {X_train_scaled.shape[0]} samples, {X_train_scaled.shape[1]} features")
    print(f"Test set: {X_test_scaled.shape[0]} samples")
    
    # Train models
    print("\n[3] Training regression models...")
    models, results = train_models(X_train_scaled, X_test_scaled, y_train, y_test)
    
    # Print results
    print("\n[4] Model Performance Results:")
    print("-" * 80)
    for model_name, result in results.items():
        print(f"\n{model_name}:")
        print(f"  MAE (Mean Absolute Error):  {result['mae']:.4f} minutes")
        print(f"  RMSE (Root Mean Squared Error): {result['rmse']:.4f} minutes")
        print(f"  R² Score: {result['r2']:.6f}")
    
    # Generate visualizations
    print("\n[5] Generating visualizations...")
    plot_delivery_distribution(df)
    plot_model_comparison(results, y_test)
    plot_predictions_vs_actual(results, y_test)
    plot_feature_importance(models, feature_cols)
    plot_traffic_impact(df)
    plot_residuals(results, y_test)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - All visualizations saved")
    print("="*80)

if __name__ == "__main__":
    main()
