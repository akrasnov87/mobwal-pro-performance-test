from locust import HttpUser, TaskSet, task
import logging
import requests as r
import files.defaultTasks as dt

userName = "qwe777"
password = "1234"

class ManagerTests(TaskSet):

    tasks = { dt.LoadMeta: 1 }

    def on_start(self):
        response = self.client.post('/auth', { "UserName": userName, "Password": password, "Version": "0.0.0.0" })
        self.client.headers.update({'RPC-Authorization': 'Token ' + response.json().get('token')})

    @task(3)
    def routePageTest(self):
        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"of_arm_pd_users","method":"Select","data":[{"params":[],"sort":[{"property":"c_login","direction":"DESC"}],"filter":[{"property":"b_disabled","value":False}],"page":1,"start":0,"limit":100000}],"type":"rpc","tid":2})
        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json=[{"action":"of_arm_cd_routes","method":"Select","data":[{"params":[],"sort":[{"property":"dx_created","direction":"DESC"}],"page":1,"start":0,"limit":20}],"type":"rpc","tid":1},{"action":"cd_templates","method":"Query","data":[{"page":1,"start":0,"limit":1000,"sort":[{"property":"n_order","direction":"ASC"}]}],"type":"rpc","tid":3},{"action":"cs_route_statuses","method":"Query","data":[{"page":1,"start":0,"limit":1000,"sort":[{"property":"n_order","direction":"ASC"}]}],"type":"rpc","tid":4}])

        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"of_arm_cd_routes","method":"Select","data":[{"params":[],"sort":[{"property":"dx_created","direction":"DESC"}],"page":1,"start":0,"limit":20}],"type":"rpc","tid":1})
        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"of_arm_cd_routes","method":"Select","data":[{"params":[],"sort":[{"property":"dx_created","direction":"DESC"}],"page":2,"start":20,"limit":20}],"type":"rpc","tid":1})
        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"of_arm_cd_routes","method":"Select","data":[{"params":[],"sort":[{"property":"dx_created","direction":"DESC"}],"page":3,"start":40,"limit":20}],"type":"rpc","tid":1})

        response = self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"of_arm_cd_routes","method":"Select","data":[{"params":[],"sort":[{"property":"dx_created","direction":"DESC"}],"page":1,"start":0,"limit":20}],"type":"rpc","tid":1})
       
        item = response.json()[0]
        records = item.get('result').get('records')
        record = records[0]

        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"cd_routes","method":"Update","data":[record],"type":"rpc","tid":5})

    @task(3)
    def taskPageTest(self):
        response = self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"of_arm_cd_routes","method":"Select","data":[{"params":[],"sort":[{"property":"dx_created","direction":"DESC"}],"page":1,"start":0,"limit":20}],"type":"rpc","tid":1})
       
        item = response.json()[0]
        records = item.get('result').get('records')
        record = records[0]

        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"of_arm_cd_routes","method":"Select","data":[{"params":[],"sort":[{"property":"dx_created","direction":"DESC"}],"page":1,"start":0,"limit":25,"filter":[{"property":"id","value":record.get('id')}]}],"type":"rpc","tid":9})
        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json=[{"action":"cd_points","method":"Query","data":[{"page":1,"start":0,"limit":25,"sort":[{"property":"n_order","direction":"ASC"}],"filter":[{"property":"fn_route","value":record.get('id')}]}],"type":"rpc","tid":8}])
        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json=[{"action":"cd_points","method":"Query","data":[{"page":2,"start":25,"limit":25,"sort":[{"property":"n_order","direction":"ASC"}],"filter":[{"property":"fn_route","value":record.get('id')}]}],"type":"rpc","tid":8}])
        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json=[{"action":"cd_points","method":"Query","data":[{"page":3,"start":50,"limit":25,"sort":[{"property":"n_order","direction":"ASC"}],"filter":[{"property":"fn_route","value":record.get('id')}]}],"type":"rpc","tid":8}])
        
        response = self.client.post('/rpc/dbo?lg=ru', name="/rpc", json=[{"action":"cd_points","method":"Query","data":[{"page":1,"start":0,"limit":25,"sort":[{"property":"n_order","direction":"ASC"}],"filter":[{"property":"fn_route","value":record.get('id')}]}],"type":"rpc","tid":8}])
        
        item = response.json()[0]
        records = item.get('result').get('records')
        record = records[0]

        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"cd_points","method":"Update","data":[{"b_check":False,"id":record.get('id')}],"type":"rpc","tid":7})
        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"cd_results","method":"Query","data":[{"params":[],"sort":[{"property":"d_date","direction":"DESC"}],"select":"id, fn_route, fn_point, fn_user, n_longitude, n_latitude, jb_data::text, c_notice, n_distance, fn_template, b_disabled, d_date, dx_created","page":1,"start":0,"limit":25,"filter":[{"property":"fn_point","value":record.get('id')}]}],"type":"rpc","tid":12})
        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"cd_templates","method":"Query","data":[{"page":1,"start":0,"limit":100000,"sort":[{"property":"n_order","direction":"ASC"}]}],"type":"rpc","tid":13})
        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"cd_attachments","method":"Query","data":[{"params":[],"sort":[{"property":"d_date","direction":"ASC"}],"select":"id, fn_user, fn_route, fn_point, fn_result, n_longitude, n_latitude, c_name, n_size, c_mime, n_distance, d_date","page":1,"start":0,"limit":25,"filter":[{"property":"fn_result","value":record.get('id')}]}],"type":"rpc","tid":12})

    @task(2)
    def collectionPageTest(self):
        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"cd_collections","method":"Query","data":[{"page":1,"start":0,"limit":25,"sort":[{"property":"c_address","direction":"ASC"}]}],"type":"rpc","tid":1})
        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"cd_collections","method":"Query","data":[{"page":2,"start":25,"limit":25,"sort":[{"property":"c_address","direction":"ASC"}]}],"type":"rpc","tid":1})
        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"cd_collections","method":"Query","data":[{"page":3,"start":50,"limit":25,"sort":[{"property":"c_address","direction":"ASC"}]}],"type":"rpc","tid":1})
        
        response = self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"cd_collections","method":"Query","data":[{"page":1,"start":0,"limit":25,"sort":[{"property":"c_address","direction":"ASC"}]}],"type":"rpc","tid":1})
        item = response.json()[0]
        records = item.get('result').get('records')
        record = records[0]

        self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"cd_collections","method":"Update","data":[record],"type":"rpc","tid":5})

    @task(1)
    def profilePageTest(self):
        response = self.client.post('/rpc?lg=ru', name="/rpc", json = {"action":"user","method":"getUser","data":[{}],"type":"rpc","tid":2})
        item = response.json()[0]
        records = item.get('result').get('records')
        record = records[0]
        serverData = { "id": record.get('id'), "c_name": record.get('c_name'), "c_post": record.get('c_post'), "c_email": record.get('c_email') }
        self.client.post('/rpc?lg=ru', name="/rpc", json = {"action":"user","method":"updateCurrentUser","data":[serverData],"type":"rpc","tid":2})

    @task(1)
    def exportTest(self):
        response = self.client.post('/rpc/dbo?lg=ru', name="/rpc", json={"action":"of_arm_cd_routes","method":"Select","data":[{"params":[],"sort":[{"property":"dx_created","direction":"DESC"}],"page":1,"start":0,"limit":20}],"type":"rpc","tid":1})
       
        item = response.json()[0]
        records = item.get('result').get('records')
        record = records[0]

        self.client.post('/rpc?lg=ru', name="/rpc", json = [{"action":"of_arm_cd_results","method":"Select","data":[{"params":[record.get('id')],"limit":100000}],"type":"rpc","tid":0}])


    @task
    def stop(self):
        self.interrupt()