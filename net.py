from Base_API_Call import API
import http.client
import json

class net_Request:
    def version(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//version"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"net_version\",\"params\":[],\"id\":67}"

        return API.Format(Call,Payload,Content,conn,form)

    def listening(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//listening"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"net_listening\",\"params\":[],\"id\":67}"

        return API.Format(Call,Payload,Content,conn,form)

    def peerCount(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//peerCount"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"net_peerCount\",\"params\":[],\"id\":74}"

        return API.Format(Call,Payload,Content,conn,form)


