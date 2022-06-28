from locust import TaskSet, task
import logging
import requests as r
import socketio
import uuid
import random
import os.path

userName = "user"
password = "1234"

class FlowException(Exception):
    pass

class MobileUser(TaskSet):
    @task(1)
    def syncTest(self):

        response = self.client.post('/auth', { "UserName": userName, "Password": password, "Version": "0.0.0.0" })
        sio = socketio.Client()

        @sio.event
        def connect_error(data):
            raise FlowException("The connection failed!")

        @sio.on('registry')
        def on_registry(data):
            items = ["7b81a216-66e7-4155-bbcb-fa6557422b5e.bkp", "9ad868cf-91bd-4cb7-a4e2-15ae14ed12ed.bkp", "53c0fceb-75c8-4d30-8fda-9a19af458c8b.bkp",
            "70cfd761-9c5c-446c-bc46-d6c6989a7503.bkp", "948fe6a6-89ff-4cb9-9b3d-22a194c0d091.bkp", "7123b14f-d651-449c-9533-78edfa0edda2.bkp", 
            "b622a9d6-6560-4717-844c-8c2f6fc0405e.bkp", "d2cd2136-d19a-4966-b009-d38cad520979.bkp"]
            with open(os.path.join("data", random.choice(items)), "rb") as f:
                bytes_read = f.read()
            sio.emit('upload', data=("1.0.0.0", bytes_read, str(uuid.uuid4()), 0, len(bytes_read)))

        @sio.on('upload')
        def on_upload(data):
            processed = data.get('meta').get('processed')

            if processed == False:
                sio.disconnect()
                raise FlowException("Файл не загружен на сервер")              

            sio.emit('synchronization', data=(data.get('tid'), "v2"))

        @sio.on('synchronization')
        def on_synchronization(data):
            processed = data.get('meta').get('processed')
            if processed == False:
                sio.disconnect()
                raise FlowException("Файл не обработан на сервере")

            sio.emit('download', data=("1.0.0.0", 0, 100 * 1024 * 1024, data.get('meta').get('tid')))

        @sio.on('download')
        def on_download(data):
            processed = data.get('meta').get('processed')
            if processed == False:
                sio.disconnect()
                raise FlowException("Файл не получен от сервера")

        base_url = self.client.base_url
        segments = base_url.replace("//", "").split("/")

        host = ""
        virtual = ""
        for idx in range(0, len(segments)):
            if idx == 0:
                host = segments[idx].replace('http:', 'ws://').replace('https:', 'wss://')
            else:
                virtual += "/" + segments[idx]

        sio.connect(host, socketio_path= virtual + "/socket.io", transports="websocket", headers={"RPC-Authorization": response.json().get('token')})

    @task
    def stop(self):
        self.interrupt()