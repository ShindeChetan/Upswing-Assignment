from fastapi import FastAPI, Query
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()

MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB = 'mqtt_data'
MONGO_COLLECTION = 'statuses'

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

#
@app.get("/status-counts/")
async def get_status_counts(start_time: str, end_time: str):
    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.fromisoformat(end_time)
    
    pipeline = [
        {"$match": {"timestamp": {"$gte": start_dt, "$lte": end_dt}}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    
    result = list(collection.aggregate(pipeline))
    status_counts = {item["_id"]: item["count"] for item in result}
    
    return status_counts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
