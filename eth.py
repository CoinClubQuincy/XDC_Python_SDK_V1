from Base_API_Call import API
import http.client
import json

class eth_Request:
    def protocolVersion(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//protocolVersion"
        Payload =  "{\"jsonrpc\":\"2.0\",\"method\":\"eth_protocolVersion\",\"params\":[],\"id\":67}"

        return API.Format(Call,Payload,Content,conn,form)

    def syncing(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//syncing"
        Payload =  "{\"jsonrpc\":\"2.0\",\"method\":\"eth_syncing\",\"params\":[],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

    def coinbase(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//coinbase"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_coinbase\",\"params\":[],\"id\":64}"

        return API.Format(Call,Payload,Content,conn,form)

    def gasPrice(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//gasPrice"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_gasPrice\",\"params\":[],\"id\":73}"

        return API.Format(Call,Payload,Content,conn,form)

    def accounts(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON",ETH_account="0x438e0b511981FE8CF7283e981ca8c3394bB3646E"):
        Call = "POST"
        Content = "//accounts"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_accounts\",\"params\":[%s],\"id\":1}" % ETH_account

        return API.Format(Call,Payload,Content,conn,form)

    def blockNumber(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//blockNumber"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_blockNumber\",\"params\":[],\"id\":83}"

        return API.Format(Call,Payload,Content,conn,form)

    def getBalance(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON",Address=""):
        Call = "POST"
        Content = "//getBalance"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getBalance\",\"params\":[\"xdce4C4FeBE1Cb34C3490167c163C9ED92049B32B5c\",\"latest\"],\"id\":1}" 

        return API.Format(Call,Payload,Content,conn,form)

#### REVIEW #### 
    def getStorageAt(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getStorageAt"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getStorageAt\",\"params\":[\"0x295a70b2de5e3953354a6a8344e616ed314d7251\",\"0x0\",\"latest\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)
#### #### #### ####
    def getTransactionCount(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getTransactionCount"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getTransactionCount\",\"params\":[\"0xbf1dcb735e512b731abd3404c15df6431bd03d42\",\"latest\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)
 
    def getBlockTransactionCountByHash(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content =  "//getBlockTransactionCountByHash"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getBlockTransactionCountByHash\",\"params\":[\"0xc8b967161c671ce952a3d50987a78d64157fb5a8e1724804b87d3e9b11e3aa34\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

    def getBlockTransactionCountByNumber(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getBlockTransactionCountByNumber"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getBlockTransactionCountByNumber\",\"params\":[\"0x52A8CA\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

    def getCode(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getCode"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getCode\",\"params\":[\"0xa94f5374fce5edbc8e2a8697c15331677e6ebf0b\",\"0x2\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

#### REVIEW #### 
    def sign(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//sign"
        Payload =  "{ \"jsonrpc\": \"2.0\", \"method\": \"eth_accounts\", \"params\": [], \"id\": 1}"
                
        return API.Format(Call,Payload,Content,conn,form)
#### #### #### ####

    def sendTransaction(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//sendTransaction"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_sendTransaction\",\"params\":[{\"from\":\"0xb60e8dd61c5d32be8058bb8eb970870f07233155\",\"to\":\"0xd46e8dd67c5d32be8058bb8eb970870f07244567\",\"gas\":\"0x76c0\",\"gasPrice\":\"0x9184e72a000\",\"value\":\"0x9184e72a\",\"data\":\"0xd46e8dd67c5d32be8d46e8dd67c5d32be8058bb8eb970870f072445675058bb8eb970870f072445675\"}],\"id\":1}"


        return API.Format(Call,Payload,Content,conn,form)

    def sendRawTransaction(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content =  "//sendRawTransaction"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_sendRawTransaction\",\"params\":[\"0xd46e8dd67c5d32be8d46e8dd67c5d32be8058bb8eb970870f072445675058bb8eb970870f072445675\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

    def call(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//call"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_call\",\"params\":[{\"from\":\"0xb60e8dd61c5d32be8058bb8eb970870f07233155\",\"to\":\"0xd46e8dd67c5d32be8058bb8eb970870f07244567\",\"gas\":\"0x76c0\",\"gasPrice\":\"0x9184e72a000\",\"value\":\"0x9184e72a\",\"data\":\"0xd46e8dd67c5d32be8d46e8dd67c5d32be8058bb8eb970870f072445675058bb8eb970870f072445675\"},\"latest\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

    def estimateGas(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content =  "//estimateGas"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_estimateGas\",\"params\":[{\"from\":\"0xb60e8dd61c5d32be8058bb8eb970870f07233155\",\"to\":\"0xd46e8dd67c5d32be8058bb8eb970870f07244567\",\"gas\":\"0x76c0\",\"gasPrice\":\"0x9184e72a000\",\"value\":\"0x9184e72a\",\"data\":\"0xd46e8dd67c5d32be8d46e8dd67c5d32be8058bb8eb970870f072445675058bb8eb970870f072445675\"}],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

    def getBlockByHash(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getBlockByHash"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getBlockByHash\",\"params\":[\"0x9326145f8a2c8c00bbe13afc7d7f3d9c868b5ef39d89f2f4e9390e9720298624\",true],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

    def getBlockByNumber(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getBlockByNumber"
        Payload =  "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getBlockByNumber\",\"params\":[\"0x0\",true],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

    def getBlockSignersByNumber(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getBlockSignersByNumber"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getBlockSignersByNumber\",\"params\":[\"0xA61F98\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

    def getBlockSignersByHash(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getBlockSignersByHash"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getBlockSignersByHash\",\"params\":[\"0x605777ee60ef3ccf21e079fa1b091b0196cf1a2c1dd7c088dd5b1ab03f680b6f\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)
 
    def getBlockFinalityByNumber(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getBlockFinalityByNumber"
        Payload =  "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getBlockFinalityByNumber\",\"params\":[\"0xA61F98\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

    def getBlockFinalityByHash(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getBlockFinalityByHash"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getBlockFinalityByHash\",\"params\":[\"0x605777ee60ef3ccf21e079fa1b091b0196cf1a2c1dd7c088dd5b1ab03f680b6f\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

    def getCandidates(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getCandidates"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getCandidates\",\"params\":[\"latest\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

    def getCandidateStatus(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getCandidateStatus"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getCandidateStatus\",\"params\":[\"0x1d50df657b6dce50bac634bf18e2d986d807e940\",\"latest\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

    def getTransactionByHash(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getTransactionByHash"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getTransactionByHash\",\"params\":[\"0xd83b26e101dd6480764bade90fc283407919f60b7e65ff83fbf6cdc92f1138a1\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

    def getTransactionByBlockHashAndIndex(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getTransactionByBlockHashAndIndex"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getTransactionByBlockHashAndIndex\",\"params\":[\"0x3c82bc62179602b67318c013c10f99011037c49cba84e31ffe6e465a21c521a7\",\"0x0\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)
 
    def getTransactionByBlockNumberAndIndex(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getTransactionByBlockNumberAndIndex"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getTransactionByBlockNumberAndIndex\",\"params\":[\"0x52A96E\",\"0x1\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)

    def getTransactionReceipt(conn=http.client.HTTPSConnection("rpc.xinfin.network"), form="JSON"):
        Call = "POST"
        Content = "//getTransactionReceipt"
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getTransactionReceipt\",\"params\":[\"0xa3ece39ae137617669c6933b7578b94e705e765683f260fcfe30eaa41932610f\"],\"id\":1}"

        return API.Format(Call,Payload,Content,conn,form)


