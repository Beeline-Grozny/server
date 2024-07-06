# AirFlow

Добавление репозитория AirFlow для helm
```bash
helm repo add airflow https://airflow.apache.org
```

Установка Helm Chart
```bash
helm install airflow airflow/airflow \
--debug \
--namespace airflow \
--create-namespace \
--set dags.gitSync.enabled=true \
--set dags.gitSync.repo=https://github.com/Beeline-Grozny/server.git \
--set dags.gitSync.branch=main \
--set dags.gitSync.subPath="/airflow/DAGs/" 
```

