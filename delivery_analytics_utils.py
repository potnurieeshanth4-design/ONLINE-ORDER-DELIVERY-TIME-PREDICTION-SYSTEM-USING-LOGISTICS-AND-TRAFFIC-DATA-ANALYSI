"""
Delivery Analytics Utilities
Generates detailed analytical datasets and insights for delivery prediction system
"""

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

def generate_delivery_dataset(n_samples=1000, random_state=42):
    """Generate synthetic delivery dataset"""
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
    
    # Generate delivery time
    delivery_time = (df['Delivery_Distance_km'] * 2.5) + \
                   (df['Traffic_Density_percent'] / 10) + \
                   (df['Order_Volume_items'] * 1.5) + \
                   (df['Number_of_Stops'] * 3) + \
                   df['Pickup_Processing_Time_min']
    
    weather_impact = df['Weather_Condition'].map({'Clear': 0, 'Rainy': 5, 'Foggy': 8, 'Snowy': 12})
    delivery_time += weather_impact
    
    priority_impact = df['Order_Priority'].map({'Standard': 0, 'Express': -3, 'Premium': -5})
    delivery_time += priority_impact
    
    delivery_time -= (df['Delivery_Partner_Experience_years'] * 0.5)
    
    time_impact = df['Time_of_Day'].map({'Morning': 2, 'Afternoon': 5, 'Evening': 3, 'Night': 8})
    delivery_time += time_impact
    
    delivery_time += np.random.normal(0, 3, n_samples)
    df['Delivery_Time_minutes'] = np.maximum(delivery_time, 10)
    
    return df

def analyze_delivery_by_priority(df):
    """Analyze delivery statistics by priority"""
    print("[1] Analyzing deliveries by priority...")
    
    stats = []
    for priority in ['Standard', 'Express', 'Premium']:
        subset = df[df['Order_Priority'] == priority]
        
        stats.append({
            'Priority': priority,
            'Total_Orders': len(subset),
            'Avg_Delivery_Time': subset['Delivery_Time_minutes'].mean(),
            'Median_Delivery_Time': subset['Delivery_Time_minutes'].median(),
            'Min_Delivery_Time': subset['Delivery_Time_minutes'].min(),
            'Max_Delivery_Time': subset['Delivery_Time_minutes'].max(),
            'Std_Dev': subset['Delivery_Time_minutes'].std()
        })
    
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv('/home/ubuntu/delivery_by_priority_stats.csv', index=False)
    print("✓ Saved: delivery_by_priority_stats.csv")
    return stats_df

def analyze_traffic_impact(df):
    """Analyze traffic impact on delivery time"""
    print("[2] Analyzing traffic impact...")
    
    # Categorize traffic
    df_traffic = df.copy()
    df_traffic['Traffic_Category'] = pd.cut(df_traffic['Traffic_Density_percent'],
                                            bins=[0, 30, 60, 100],
                                            labels=['Low', 'Medium', 'High'])
    
    stats = []
    for traffic_cat in ['Low', 'Medium', 'High']:
        subset = df_traffic[df_traffic['Traffic_Category'] == traffic_cat]
        
        stats.append({
            'Traffic_Category': traffic_cat,
            'Sample_Count': len(subset),
            'Avg_Delivery_Time': subset['Delivery_Time_minutes'].mean(),
            'Avg_Traffic_Density': subset['Traffic_Density_percent'].mean(),
            'Avg_Distance': subset['Delivery_Distance_km'].mean()
        })
    
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv('/home/ubuntu/delivery_traffic_impact_stats.csv', index=False)
    print("✓ Saved: delivery_traffic_impact_stats.csv")
    return stats_df

def analyze_weather_impact(df):
    """Analyze weather impact on delivery time"""
    print("[3] Analyzing weather impact...")
    
    stats = []
    for weather in df['Weather_Condition'].unique():
        subset = df[df['Weather_Condition'] == weather]
        
        stats.append({
            'Weather_Condition': weather,
            'Total_Orders': len(subset),
            'Avg_Delivery_Time': subset['Delivery_Time_minutes'].mean(),
            'Avg_Distance': subset['Delivery_Distance_km'].mean(),
            'Avg_Traffic': subset['Traffic_Density_percent'].mean()
        })
    
    stats_df = pd.DataFrame(stats).sort_values('Avg_Delivery_Time', ascending=False)
    stats_df.to_csv('/home/ubuntu/delivery_weather_impact_stats.csv', index=False)
    print("✓ Saved: delivery_weather_impact_stats.csv")
    return stats_df

def analyze_time_of_day_impact(df):
    """Analyze time of day impact"""
    print("[4] Analyzing time of day impact...")
    
    stats = []
    for time_period in ['Morning', 'Afternoon', 'Evening', 'Night']:
        subset = df[df['Time_of_Day'] == time_period]
        
        stats.append({
            'Time_Period': time_period,
            'Total_Orders': len(subset),
            'Avg_Delivery_Time': subset['Delivery_Time_minutes'].mean(),
            'Avg_Traffic': subset['Traffic_Density_percent'].mean(),
            'Avg_Orders_per_Stop': subset['Order_Volume_items'].mean()
        })
    
    stats_df = pd.DataFrame(stats)
    stats_df.to_csv('/home/ubuntu/delivery_time_of_day_stats.csv', index=False)
    print("✓ Saved: delivery_time_of_day_stats.csv")
    return stats_df

def analyze_vehicle_performance(df):
    """Analyze vehicle type performance"""
    print("[5] Analyzing vehicle performance...")
    
    stats = []
    for vehicle in df['Vehicle_Type'].unique():
        subset = df[df['Vehicle_Type'] == vehicle]
        
        stats.append({
            'Vehicle_Type': vehicle,
            'Total_Deliveries': len(subset),
            'Avg_Delivery_Time': subset['Delivery_Time_minutes'].mean(),
            'Avg_Distance': subset['Delivery_Distance_km'].mean(),
            'Avg_Stops': subset['Number_of_Stops'].mean()
        })
    
    stats_df = pd.DataFrame(stats).sort_values('Avg_Delivery_Time')
    stats_df.to_csv('/home/ubuntu/delivery_vehicle_performance.csv', index=False)
    print("✓ Saved: delivery_vehicle_performance.csv")
    return stats_df

def generate_operational_insights(df):
    """Generate operational insights"""
    print("[6] Generating operational insights...")
    
    insights = []
    
    insights.append("ONLINE ORDER DELIVERY TIME PREDICTION SYSTEM - OPERATIONAL INSIGHTS")
    insights.append("="*70)
    
    insights.append(f"\nTotal Orders Analyzed: {len(df)}")
    insights.append(f"Average Delivery Time: {df['Delivery_Time_minutes'].mean():.2f} minutes")
    insights.append(f"Median Delivery Time: {df['Delivery_Time_minutes'].median():.2f} minutes")
    insights.append(f"Standard Deviation: {df['Delivery_Time_minutes'].std():.2f} minutes")
    
    insights.append("\n\nDelivery Time by Priority:")
    insights.append("-" * 70)
    for priority in ['Standard', 'Express', 'Premium']:
        subset = df[df['Order_Priority'] == priority]
        avg_time = subset['Delivery_Time_minutes'].mean()
        insights.append(f"  {priority}: {avg_time:.2f} minutes (n={len(subset)})")
    
    insights.append("\n\nWeather Impact Analysis:")
    insights.append("-" * 70)
    for weather in df['Weather_Condition'].unique():
        subset = df[df['Weather_Condition'] == weather]
        avg_time = subset['Delivery_Time_minutes'].mean()
        insights.append(f"  {weather}: {avg_time:.2f} minutes (n={len(subset)})")
    
    insights.append("\n\nKey Performance Indicators:")
    insights.append("-" * 70)
    
    express_orders = df[df['Order_Priority'] == 'Express']
    express_on_time = (express_orders['Delivery_Time_minutes'] < 60).sum() / len(express_orders) * 100
    insights.append(f"  Express Orders On-Time Rate (<60 min): {express_on_time:.1f}%")
    
    premium_orders = df[df['Order_Priority'] == 'Premium']
    premium_on_time = (premium_orders['Delivery_Time_minutes'] < 45).sum() / len(premium_orders) * 100
    insights.append(f"  Premium Orders On-Time Rate (<45 min): {premium_on_time:.1f}%")
    
    long_distance = df[df['Delivery_Distance_km'] > 30]
    insights.append(f"  Average Time for Long Distance (>30 km): {long_distance['Delivery_Time_minutes'].mean():.2f} minutes")
    
    high_traffic = df[df['Traffic_Density_percent'] > 75]
    insights.append(f"  Average Time in High Traffic (>75%): {high_traffic['Delivery_Time_minutes'].mean():.2f} minutes")
    
    # Write insights to file
    with open('/home/ubuntu/delivery_operational_insights.txt', 'w') as f:
        f.write('\n'.join(insights))
    
    print("✓ Saved: delivery_operational_insights.txt")
    return insights

def generate_sample_predictions(df):
    """Generate sample delivery predictions"""
    print("[7] Generating sample predictions...")
    
    predictions = []
    
    scenarios = [
        {'Distance': 5, 'Traffic': 20, 'Priority': 'Express', 'Weather': 'Clear'},
        {'Distance': 15, 'Traffic': 50, 'Priority': 'Standard', 'Weather': 'Rainy'},
        {'Distance': 30, 'Traffic': 80, 'Priority': 'Standard', 'Weather': 'Foggy'},
        {'Distance': 10, 'Traffic': 30, 'Priority': 'Premium', 'Weather': 'Clear'},
        {'Distance': 25, 'Traffic': 60, 'Priority': 'Express', 'Weather': 'Snowy'},
    ]
    
    for i, scenario in enumerate(scenarios):
        # Estimate delivery time
        est_time = (scenario['Distance'] * 2.5) + (scenario['Traffic'] / 10)
        
        weather_impact = {'Clear': 0, 'Rainy': 5, 'Foggy': 8, 'Snowy': 12}
        est_time += weather_impact[scenario['Weather']]
        
        priority_impact = {'Standard': 0, 'Express': -3, 'Premium': -5}
        est_time += priority_impact[scenario['Priority']]
        
        predictions.append({
            'Scenario_ID': i + 1,
            'Delivery_Distance_km': scenario['Distance'],
            'Traffic_Density_percent': scenario['Traffic'],
            'Order_Priority': scenario['Priority'],
            'Weather_Condition': scenario['Weather'],
            'Estimated_Time_minutes': max(10, est_time),
            'Confidence_Level': 'High' if est_time < 100 else 'Medium'
        })
    
    pred_df = pd.DataFrame(predictions)
    pred_df.to_csv('/home/ubuntu/delivery_sample_predictions.csv', index=False)
    print("✓ Saved: delivery_sample_predictions.csv")
    return pred_df

def main():
    print("="*80)
    print("DELIVERY ANALYTICS UTILITIES - GENERATING DETAILED DATASETS")
    print("="*80)
    print()
    
    # Generate main dataset
    print("Generating delivery dataset...")
    df = generate_delivery_dataset(n_samples=1000)
    df.to_csv('/home/ubuntu/delivery_full_dataset.csv', index=False)
    print(f"✓ Dataset created: {df.shape[0]} records\n")
    
    # Generate analytical datasets
    analyze_delivery_by_priority(df)
    analyze_traffic_impact(df)
    analyze_weather_impact(df)
    analyze_time_of_day_impact(df)
    analyze_vehicle_performance(df)
    generate_operational_insights(df)
    generate_sample_predictions(df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - All datasets generated successfully")
    print("="*80)

if __name__ == "__main__":
    main()
