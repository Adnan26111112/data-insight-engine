def generate_insights(df):
    insights = []

    for col in df.select_dtypes(include=['number']).columns:
        mean = df[col].mean()
        max_val = df[col].max()
        min_val = df[col].min()

        insights.append(
            f"{col}: Avg = {mean:.2f}, Max = {max_val}, Min = {min_val}"
        )

    return insights