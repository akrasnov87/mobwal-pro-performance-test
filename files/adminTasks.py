from locust import HttpUser, TaskSet, task
import logging
import requests as r
import files.defaultTasks as dt

userName = "admin"
password = "qwe-123"

class AdminTests(TaskSet):

    tasks = { dt.LoadMeta: 1 }

    def on_start(self):
        response = self.client.post('/auth', { "UserName": userName, "Password": password, "Version": "0.0.0.0" })
        self.client.headers.update({'RPC-Authorization': 'Token ' + response.json().get('token')})

    @task(1)
    def settingPageTest(self):
        response = self.client.post('/rpc/core?lg=ru', name="/rpc", json={"action":"sd_settings","method":"Query","data":[{"page":1,"start":0,"limit":25}],"type":"rpc","tid":1})
        item = response.json()[0]
        records = item.get('result').get('records')
        record = records[0]
        self.client.post('/rpc/core?lg=ru', name="/rpc", json = {"action":"sd_settings","method":"Update","data":[record],"type":"rpc","tid":2})

    @task(1)
    def profilePageTest(self):
        response = self.client.post('/rpc?lg=ru', name="/rpc", json = {"action":"user","method":"getUser","data":[{}],"type":"rpc","tid":2})
        item = response.json()[0]
        records = item.get('result').get('records')
        record = records[0]
        serverData = { "id": record.get('id'), "c_name": record.get('c_name'), "c_post": record.get('c_post'), "c_email": record.get('c_email') }
        self.client.post('/rpc?lg=ru', name="/rpc", json = {"action":"user","method":"updateCurrentUser","data":[serverData],"type":"rpc","tid":2})

    @task(2)
    def templatePageTest(self):
        response = self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"cd_templates","method":"Query","data":[{"page":1,"start":0,"limit":25,"sort":[{"property":"c_template","direction":"ASC"}]}],"type":"rpc","tid":4})
        item = response.json()[0]
        records = item.get('result').get('records')
        record = records[0]
        self.client.post('/rpc?lg=ru', name="/rpc", json = {"action":"cd_templates", "method":"Update", "data":[record], "type":"rpc", "tid":2})

    @task(1)
    def levelPageTest(self):
        response = self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"shell","method":"levels","data":[{"node":"root"}],"type":"rpc","tid":6})
        item = response.json()[0]
        record = item.get('data')[0]
        self.client.post('/rpc?lg=ru', name="/rpc", json = {"action":"shell","method":"levels","data":[{"node": record.get('id')}],"type":"rpc","tid":2})

    @task(6)
    def userPageTest(self):
        response = self.client.post('/rpc/core?lg=ru', name="/rpc", json={"action":"of_level_users","method":"Select","data":[{"params":[],"sort":[{"property":"c_login","direction":"DESC"}],"filter":[{"property":"b_disabled","value":False}],"page":1,"start":0,"limit":25}],"type":"rpc","tid":1})
        item = response.json()[0]
        records = item.get('result').get('records')
        record = records[0]
        self.client.post('/rpc/core?lg=ru', name="/rpc", json={"action":"of_level_users","method":"Select","data":[{"params":[],"sort":[{"property":"c_login","direction":"DESC"}],"page":1,"start":0,"limit":25}],"type":"rpc","tid":1})
        self.client.post('/rpc/core?lg=ru', name="/rpc", json={"action":"pd_roles","method":"Query","data":[{"params":[],"sort":[{"property":"n_weight","direction":"DESC"}],"filter":[{"property":"sn_delete","value":False}],"page":1,"start":0,"limit":100}],"type":"rpc","tid":6})
        self.client.post('/rpc?lg=ru', name="/rpc", json = {"action":"user","method":"updateOtherUser","data":[{"id":record.get('id'),"f_level":record.get('f_level')}],"type":"rpc","tid":12})
        
    @task
    def stop(self):
        self.interrupt()