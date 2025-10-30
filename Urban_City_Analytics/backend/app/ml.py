from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import pandas as pd
from io import BytesIO
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

ml_router = APIRouter()

@ml_router.post("/insight")
async def ml_insight(file: UploadFile = File(...), ml_type: str = Form(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(BytesIO(contents))
        result = {}

        numeric_cols = df.select_dtypes(include="number").columns

        if ml_type == "population":
            if len(numeric_cols) >= 2:
                X = df[[numeric_cols[0]]].values
                y = df[numeric_cols[1]].values
                model = LinearRegression()
                model.fit(X, y)
                result["prediction"] = model.predict(X).tolist()
            else:
                raise HTTPException(status_code=400, detail="Not enough numeric columns for population prediction")

        elif ml_type == "traffic":
            if len(numeric_cols) > 0:
                X = df[[numeric_cols[0]]].values
                y = df[numeric_cols[0]].values
                model = LinearRegression()
                model.fit(X, y)
                result["prediction"] = model.predict(X).tolist()
            else:
                raise HTTPException(status_code=400, detail="No numeric columns for traffic prediction")

        elif ml_type == "air_quality":
            if len(numeric_cols) > 0:
                X = df[numeric_cols].values
                target = pd.cut(df[numeric_cols[0]], bins=3, labels=["Good", "Moderate", "Unhealthy"])
                le = LabelEncoder()
                y = le.fit_transform(target)
                model = DecisionTreeClassifier()
                model.fit(X, y)
                result["prediction"] = le.inverse_transform(model.predict(X)).tolist()
            else:
                raise HTTPException(status_code=400, detail="No numeric columns for air quality classification")

        elif ml_type == "infrastructure":
            numeric_df = df.select_dtypes(include="number")
            if not numeric_df.empty:
                kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
                clusters = kmeans.fit_predict(numeric_df)
                result["clusters"] = clusters.tolist()
            else:
                raise HTTPException(status_code=400, detail="No numeric columns for clustering")
        else:
            raise HTTPException(status_code=400, detail="Invalid ML type")

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ML insight: {str(e)}")
