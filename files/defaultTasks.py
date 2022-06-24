from locust import HttpUser, TaskSet, task, between, constant
import logging
import requests as r

class LoadMeta(TaskSet):
    @task
    def meta(self):
        self.client.get('/rpc/meta?lg=ru', name="/rpc/meta")

    @task
    def core(self):
        self.client.get('/rpc/meta/core?lg=ru', name="/rpc/meta")

    @task
    def dbo(self):
        self.client.get('/rpc/meta/dbo?lg=ru', name="/rpc/meta")

    @task
    def stop(self):
        self.interrupt()