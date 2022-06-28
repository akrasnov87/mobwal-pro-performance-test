from locust import HttpUser, TaskSet, task, between, constant
import logging
import tests.adminTasks as at
import tests.managerTasks as mt
import tests.userTasks as ut
import tests.mobileTasks as mobt

class AdminUser(HttpUser):
    wait_time = constant(1)

    tasks = { at.AdminTests: 1 }

class ManagerUser(HttpUser):
    wait_time = constant(1)

    tasks = { mt.ManagerTests: 1 }

class SimpleUser(HttpUser):
    wait_time = constant(1)

    tasks = { ut.UserTests: 1 }

class MobileUser(HttpUser):
    wait_time = constant(1)

    tasks = { mobt.MobileUser: 1 }