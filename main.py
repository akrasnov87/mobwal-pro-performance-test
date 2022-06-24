from locust import HttpUser, TaskSet, task, between, constant
import logging
import files.adminTasks as at
import files.managerTasks as mt
import files.userTasks as ut
import requests as r
from locust_plugins.users import SocketIOUser
import time
import json
import socketio
import uuid

'''
class AdminUser(HttpUser):
    wait_time = constant(1)

    tasks = { at.AdminTests: 1 }

class ManagerUser(HttpUser):
    wait_time = constant(1)

    tasks = { mt.ManagerTests: 1 }

class SimpleUser(HttpUser):
    wait_time = constant(1)

    tasks = { ut.UserTests: 1 }
'''

userName = "user"
password = "1234"

class FlowException(Exception):
    pass

class MobileUser(HttpUser):
    wait_time = constant(1)

    @task(1)
    def test_my(self):
        response = self.client.post('/auth', { "UserName": userName, "Password": password, "Version": "0.0.0.0" })
        sio = socketio.Client()
        self.client.uuid = str(uuid.uuid4())

        @sio.event
        def connect_error(data):
            raise FlowException("The connection failed!")

        @sio.on('registry')
        def on_registry(data):
            with open("data.bkp", "rb") as f:
                bytes_read = f.read()

            sio.emit('upload', data=("1.0.0.0", bytes_read, self.client.uuid, 0, len(bytes_read)))

        @sio.on('upload')
        def on_upload(data):
            sio.emit('synchronization', data=(self.client.uuid, "v2"))

        @sio.on('synchronization')
        def on_synchronization(data):
            sio.emit('download', data=("1.0.0.0", 0, 10 * 1024 * 1024, self.client.uuid))

        @sio.on('download')
        def on_download(data):
            processed = data.get('meta').get('processed')
            if processed == False:
                FlowException("Файл не получен от сервера")
            else:
                sio.disconnect()

        sio.connect('ws://localhost:5007', socketio_path="/release/socket.io", transports="websocket", headers={"RPC-Authorization": response.json().get('token')})