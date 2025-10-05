import pandas as pd
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json

# Instantiate FastAPI application
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],  # Allows POST and OPTIONS requests
    allow_headers=["*"],  # Allows all headers
)

# Load the telemetry data from a file
with open('telemetry.json') as f:
    telemetry_data = json.load(f)
    df = pd.DataFrame(telemetry_data)

@app.post("/api")
async def get_metrics(request: Request):
    data = await request.json()
    regions = data.get("regions", [])
    threshold_ms = data.get("threshold_ms", 180)

    # Filter data by regions
    filtered_df = df[df['region'].isin(regions)]
    
    # Calculate metrics per region
    metrics = []
    for region in regions:
        region_df = filtered_df[filtered_df['region'] == region]
        if not region_df.empty:
            avg_latency = region_df['latency_ms'].mean()
            p95_latency = region_df['latency_ms'].quantile(0.95)
            avg_uptime = region_df['is_online'].mean()
            breaches = (region_df['latency_ms'] > threshold_ms).sum()
            
            metrics.append({
                "region": region,
                "avg_latency": avg_latency,
                "p95_latency": p95_latency,
                "avg_uptime": avg_uptime,
                "breaches": int(breaches)
            })
    
    return metrics
