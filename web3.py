from Base_API_Call import API
import http.client

class web3_Request:
    def clientVersion(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//version"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"net_version\",\"params\":[],\"id\":67}"
        
        return API.Format(Call,Payload,Content,conn,form)

    def sha3(conn=http.client.HTTPSConnection("rpc.xinfin.network"),form ="JSON",Hash=""):
        Call = "POST"
        Content = "//sha3"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"web3_sha3\",\"params\":[\"0x%s\"],\"id\":64}" % Hash

        return API.Format(Call,Payload,Content,conn,form)