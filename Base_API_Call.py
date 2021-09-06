import json
import http.client

class API:
    def Call(call,payload,content,conn):
        headers = { 'content-type': "application/json" }

        conn.request(call, content, payload, headers)
        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")

    def Request_formatter(JSON):
        Item = json.loads(JSON)
        jsonrpc = Item["jsonrpc"]
        id = Item["id"]
        result = Item["result"]

        return result    

    def Format(Call,Payload,Content,conn,form):
        #Try 
        if conn == "test":
            conn = "test"
            if form == "JSON":
                return API.Call(Call,Payload,Content,conn)
            else:
                JSON = API.Call(Call,Payload,Content,conn)
                return API.clientVersion_formatter(JSON)
        
        else:
            if form == "JSON":
                return API.Call(Call,Payload,Content,conn)
            else:
                JSON = API.Call(Call,Payload,Content,conn)
                return API.Request_formatter(JSON)
        #Except
            ##ERROR Handling

    def Tatum_Format():
        print("Base API")

    def Tatum_Request_Formater():
        print("Base API")


