from locust import HttpUser, TaskSet, task, between, constant
import logging
import files.adminTasks as at
import files.managerTasks as mt
import files.userTasks as ut
import requests as r

class AdminUser(HttpUser):
    wait_time = constant(1)

    tasks = { at.AdminTests: 1 }

class ManagerUser(HttpUser):
    wait_time = constant(1)

    tasks = { mt.ManagerTests: 1 }

class SimpleUser(HttpUser):
    wait_time = constant(1)

    tasks = { ut.UserTests: 1 }