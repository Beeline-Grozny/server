from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime
from airflow import DAG
import os

os.system("docker build -t rs-image-normalization:latest -f docker/normalization.Dockerfile .")

with DAG(
    dag_id="image-normalization",
    schedule=None,
    start_date=datetime.now(),
    catchup=False,
    tags=["example"],
) as dag:
    airflow_with_kubernetes = KubernetesPodOperator(
        name="kubernetes_operator",
        image="rs-image-normalization:latest",
        cmds=["python"],
        arguments=["main.py"],
        task_id="run-pod-image-normalization",
    )

airflow_with_kubernetes.dry_run()