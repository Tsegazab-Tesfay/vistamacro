from vista_macro.configuration.mongo_db_connection import MongoDBClient
from vista_macro.pipeline.training_pipeline import TrainPipeline
from vista_macro.ml.model.estimator import ModelResolver,TargetValueMapping
from vista_macro.utils.main_utils import load_object
from vista_macro.constant.training_pipeline import SAVED_MODEL_DIR

import pandas as pd
import numpy as np

from fastapi import FastAPI
from vista_macro.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response

app = FastAPI()


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.get("/predict")
async def predict_route():
    try:
        #get data from user csv file
        #conver csv file to dataframe
        df = pd.read_csv("/Users/tt/Documents/VISTAMACRO/vistamacro/artifact/01_12_2025_14_11_38/data_ingestion/ingested/test.csv")
        columns_to_drop = ["class"]
        # if "_id" in df.columns.to_list():
        #     df = df.drop(columns=["_id"], axis=1)
        for col in columns_to_drop:
            if col in df.columns.to_list():
                df = df.drop(columns=[col], axis=1)

        df.replace({"na": np.nan}, inplace=True)
        #df=None
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        
        #decide how to return file to user.
        print(df.head())
        
    except Exception as e:
        raise Response(f"Error Occured! {e}")

if __name__ == "__main__":
    # mongodb_client = MongoDBClient()
    # print(mongodb_client.database.list_collection_names())

    # training_pipeline = TrainPipeline()
    # training_pipeline.run_pipeline()
    app_run(app, host=APP_HOST, port=APP_PORT)