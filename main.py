from locust import HttpUser, TaskSet, task, between, constant
import logging
import files.adminTasks as at
import files.managerTasks as mt
import files.userTasks as ut
import requests as r

class AdminUser(HttpUser):
    wait_time = constant(1)

    tasks = { at.AdminTests: 2, mt.ManagerTests: 2, ut.UserTests: 20 }

    @task(1)
    def exists(i):
        with i.client.get('/exists', catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f'status code is {response.status_code}')