from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os

os.system("pip install roboflow ultralytics")

from roboflow import Roboflow
from ultralytics import YOLO
from ultralytics import settings

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 6),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'yolov8_pipeline',
    default_args=default_args,
    description='A simple DAG to train YOLOv8 model',
    schedule_interval=timedelta(days=1),
)

def download_dataset():
    rf = Roboflow(api_key="KdzwPt1kMDiWW0rj6uv7")
    project = rf.workspace("idk-ocra0").project("bfhdofg")
    version = project.version(1)
    dataset = version.download("yolov8")
    os.environ['DATASET_PATH'] = dataset.location
    print(f"Dataset downloaded and unpacked to: {dataset.location}")

def train_model():
    settings.update({
        'mlflow': True,
        'clearml': False,
        'comet': False,
        'dvc': False,
        'hub': False,
        'neptune': False,
        'raytune': False,
        'tensorboard': False,
        'wandb': False
    })

    os.system("export MLFLOW_TRACKING_URI=http://localhost:5000")
    os.system("export MLFLOW_EXPERIMENT_NAME=Classification")
    os.system("export MLFLOW_RUN=prod-model")

    dataset_path = os.getenv('DATASET_PATH')
    model = YOLO("yolov8n-pose.yaml")
    model.train(data=dataset_path, epochs=20)  # Настройте параметры тренировки по необходимости
    model.save("trained_yolov8_model.pt")
    print("Model trained and saved.")

def validate_model():
    model = YOLO("trained_yolov8_model.pt")
    results = model.val()
    print("Validation results:", results)

download_dataset_task = PythonOperator(
    task_id='download_dataset',
    python_callable=download_dataset,
    dag=dag,
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag,
)

validate_model_task = PythonOperator(
    task_id='validate_model',
    python_callable=validate_model,
    dag=dag,
)

download_dataset_task >> train_model_task >> validate_model_task
