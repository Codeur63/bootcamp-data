Mettre a jour la base ou l'initailiser
```uv run airflow db init```
```uv run airflow db migrate```

creer un utilisateur airflow
```uv run airflow users create ... ```

Verifier les lists dags avec docker (Adaptez en conction de votre version docker)
```sudo docker-compose exec airflow-scheduler airflow dags list```

