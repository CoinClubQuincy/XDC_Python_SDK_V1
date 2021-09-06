from Base_API_Call import API
import http.client
import json

conn = http.client.HTTPSConnection("api-eu1.tatum.io")

class tatum_Request():
    def Generate_XDC_Wallet(Seed, API_KEY,form="JSON"):
        headers = { 'x-api-key': API_KEY }
        conn.request("GET", "/v3/xdc/wallet?mnemonic=%s" % Seed, headers=headers)

        res = conn.getresponse()
        data = res.read()

        if form == "JSON":
            return data.decode("utf-8")
        else:
            DATA = data.decode("utf-8")
            Item = json.loads(DATA)
            
            xpub = Item["xpub"]
            mnemonic =Item["mnemonic"]

            return xpub

############ TEST ############
    def Generate_XDC_Wallet_EPK(API_KEY,xpub,index,form="JSON"):
        headers = { 'x-api-key': API_KEY }
        conn.request("GET", "/v3/xdc/address/%s/%s" % (xpub,index), headers=headers)
        res = conn.getresponse()
        data = res.read()

        if form == "JSON":
            return data.decode("utf-8")
        else:
            DATA = data.decode("utf-8")
            Item = json.loads(DATA)
            address = Item["address"]

            return address

    def Generate_XDC_Private_key(API_KEY,Seed,form="JSON"):
        payload = "{\"index\":0,\"mnemonic\":\"%s\"}" % Seed
        headers = {
            'content-type': "application/json",
            'x-api-key': API_KEY
            }

        conn.request("POST", "/v3/xdc/wallet/priv", payload, headers)
        res = conn.getresponse()
        data = res.read()

        if form == "JSON":
            return data.decode("utf-8")
        else:
            DATA = data.decode("utf-8")
            Item = json.loads(DATA)
            key = Item["key"] 

            return key

    def Web3_HTTP_Driver(ApiKey,form="JSON"):
        Call = "POST"
        Content = "/v3/xdc/web3/%s" % ApiKey
        Payload = "{\"jsonrpc\":\"2.0\",\"method\":\"web3_clientVersion\",\"params\":[],\"id\":2}"

        return API.Format(Call,Payload,Content,conn,form)

    def Current_Block_Number(API_Key,form="JSON"):
        conn = http.client.HTTPSConnection("api-eu1.tatum.io")
        headers = { 'x-api-key': API_Key }
        conn.request("GET", "/v3/xdc/block/current", headers=headers)
        res = conn.getresponse()
        data = res.read()

        return (data.decode("utf-8"))

####### TEST #######
    def XDC_Block_by_Hash(API_KEY,Hash,form="JSON"):
        conn = http.client.HTTPSConnection("api-eu1.tatum.io")
        headers = { 'x-api-key': API_KEY }
        conn.request("GET", "/v3/xdc/block/%s" % Hash, headers=headers)
        res = conn.getresponse()
        data = res.read()

        return (data.decode("utf-8"))

    def XDC_Account_Balance(API_KEY,Address,form="JSON"):
        conn = http.client.HTTPSConnection("api-eu1.tatum.io")
        headers = { 'x-api-key': API_KEY }
        conn.request("GET", "/v3/xdc/account/balance/%s" % Address, headers=headers)
        res = conn.getresponse()
        data = res.read()

        if form == "Text":
            Item = json.loads(data.decode("utf-8"))
            balance = Item["balance"]
            return balance
        else:
            return (data.decode("utf-8"))

    def  XDC_Transaction(API_KEY,Hash,form="JSON"):
        conn = http.client.HTTPSConnection("api-eu1.tatum.io")
        headers = { 'x-api-key': API_KEY }
        conn.request("GET", "/v3/xdc/transaction/%s" % Hash, headers=headers)
        res = conn.getresponse()
        data = res.read()

        if form == "Text":
            Item = json.loads(data.decode("utf-8")) 
            blockHash = Item["blockHash"]   
            blockNumber = Item["blockNumber"]  
            From = Item["from"]  
            gas = Item["gas"]  
            gasPrice = Item["gasPrice"]  
            input = Item["input"]  
            nonce = Item["nonce"]  
            To = Item["to"]  
            transactionIndex = Item["transactionIndex"]  
            value = Item["value"]  
            contractAddress = Item["contractAddress"]  
            cumulativeGasUsed = Item["cumulativeGasUsed"]  
            gasUsed = Item["gasUsed"]  
            logs = Item["logs"]  

            return [blockHash,blockNumber,From,gas,gasPrice,input,nonce,To,transactionIndex,value,contractAddress,cumulativeGasUsed,gasUsed,logs]
        else:
            return (data.decode("utf-8"))

    def Count_Outgoing_XDC_Transactions(API_KEY,Address,form="JSON"):
        conn = http.client.HTTPSConnection("api-eu1.tatum.io")
        headers = { 'x-api-key': API_KEY }
        conn.request("GET", "/v3/xdc/transaction/count/%s" % Address, headers=headers)
        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")

####### TEST #######
    def Send_XDC_ERC20(API_KEY,form="JSON"):
        conn = http.client.HTTPSConnection("api-eu1.tatum.io")
        payload = "{\"data\":\"My note to recipient.\",\"nonce\":0,\"to\":\"xdc687422eEA2cB73B5d3e242bA5456b782919AFc85\",\"fee\":{\"gasLimit\":\"40000\",\"gasPrice\":\"20\"},\"amount\":\"100000\",\"fromPrivateKey\":\"0x05e150c73f1920ec14caa1e0b6aa09940899678051a78542840c2668ce5080c2\"}"
        headers = {
            'content-type': "application/json",
            'x-api-key': API_KEY
            }
        conn.request("POST", "/v3/xdc/transaction", payload, headers)
        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")

####### TEST #######
    def Estimate_XDC_Transaction_Fees(API_KEY,Address1,Address2,form="JSON"):
        conn = http.client.HTTPSConnection("api-eu1.tatum.io")
        payload = "{\"from\":\"xdcfb99f8ae9b70a0c8cd96ae665bbaf85a7e01a2ef\",\"to\":\"xdc687422eEA2cB73B5d3e242bA5456b782919AFc85\",\"amount\":\"100000\",\"data\":\"My note to recipient.\"}"
        headers = {
            'content-type': "application/json",
            'x-api-key': API_KEY
            }
        conn.request("POST", "/v3/xdc/gas", payload, headers)
        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")

####### TEST #######
    def Execute_Smart_Contract(API_KEY,contractAddress,form="JSON"):
        conn = http.client.HTTPSConnection("api-eu1.tatum.io")
        payload = "{\"contractAddress\":\"xdc687422eEA2cB73B5d3e242bA5456b782919AFc85\",\"methodName\":\"transfer\",\"methodABI\":{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"amount\",\"type\":\"uint256\"}],\"name\":\"stake\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},\"params\":[\"0x632\"]}"
        headers = {
            'content-type': "application/json",
            'x-api-key': API_KEY
            }

        conn.request("POST", "/v3/xdc/smartcontract", payload, headers)
        res = conn.getresponse()
        data = res.read()

        return (data.decode("utf-8"))

####### TEST #######
    def Broadcast_Signed_XDC_Transaction(API_KEY,txData,signatureId,form="JSON"):
        conn = http.client.HTTPSConnection("api-eu1.tatum.io")
        payload = "{\"txData\":\"62BD544D1B9031EFC330A3E855CC3A0D51CA5131455C1AB3BCAC6D243F65460D\",\"signatureId\":\"1f7f7c0c-3906-4aa1-9dfe-4b67c43918f6\"}"
        headers = {
            'content-type': "application/json",
            'x-api-key': API_KEY
            }

        conn.request("POST", "/v3/xdc/broadcast", payload, headers)
        res = conn.getresponse()
        data = res.read()

        return (data.decode("utf-8"))
