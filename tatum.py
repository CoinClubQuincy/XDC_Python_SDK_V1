from Base_API_Call import API, APIError
import json
from urllib.parse import quote

TATUM_HOST = "api-eu1.tatum.io"


def _request(call, path, API_KEY, payload=None, conn=None):
    """Sends one request to Tatum. API_KEY never appears in an error message."""
    API.required("API_KEY", API_KEY)
    body = None if payload is None else json.dumps(payload)
    own_connection = conn is None
    if own_connection:
        conn = API.Connect(TATUM_HOST)
    try:
        return API.Call(call, body, path, conn, headers={"x-api-key": API_KEY})
    finally:
        if own_connection:
            conn.close()


def _field(text, name):
    try:
        return json.loads(text)[name]
    except (ValueError, KeyError, TypeError) as error:
        raise APIError("Response has no %s" % name) from error


def _path(value):
    return quote(str(API.required("value", value)), safe="")


class tatum_Request():
    def Generate_XDC_Wallet(Seed, API_KEY, form="JSON", conn=None):
        """Sends the seed to Tatum. Use a test seed, and never one holding real funds."""
        API.required("Seed", Seed)
        text = _request("GET", "/v3/xdc/wallet?mnemonic=%s" % quote(Seed, safe=""), API_KEY, conn=conn)
        return text if form == "JSON" else _field(text, "xpub")

    def Generate_XDC_Wallet_EPK(API_KEY, xpub, index, form="JSON", conn=None):
        text = _request("GET", "/v3/xdc/address/%s/%s" % (_path(xpub), int(index)), API_KEY, conn=conn)
        return text if form == "JSON" else _field(text, "address")

    def Generate_XDC_Private_key(API_KEY, Seed, form="JSON", index=0, conn=None):
        """Sends the seed to Tatum and gets a private key back. Use a test seed only."""
        API.required("Seed", Seed)
        text = _request("POST", "/v3/xdc/wallet/priv", API_KEY, {"index": int(index), "mnemonic": Seed}, conn)
        return text if form == "JSON" else _field(text, "key")

    def Web3_HTTP_Driver(ApiKey, form="JSON", conn=None):
        """Tatum takes the key in the URL here, so it can end up in proxy and server logs."""
        API.required("ApiKey", ApiKey)
        own_connection = conn is None
        if own_connection:
            conn = API.Connect(TATUM_HOST)
        try:
            return API.Format("web3_clientVersion", [], conn, form, id=2, content="/v3/xdc/web3/%s" % _path(ApiKey))
        finally:
            if own_connection:
                conn.close()

    def Current_Block_Number(API_Key, form="JSON", conn=None):
        return _request("GET", "/v3/xdc/block/current", API_Key, conn=conn)

    def XDC_Block_by_Hash(API_KEY, Hash, form="JSON", conn=None):
        return _request("GET", "/v3/xdc/block/%s" % _path(Hash), API_KEY, conn=conn)

    def XDC_Account_Balance(API_KEY, Address, form="JSON", conn=None):
        text = _request("GET", "/v3/xdc/account/balance/%s" % _path(Address), API_KEY, conn=conn)
        return text if form == "JSON" else _field(text, "balance")

    def XDC_Transaction(API_KEY, Hash, form="JSON", conn=None):
        text = _request("GET", "/v3/xdc/transaction/%s" % _path(Hash), API_KEY, conn=conn)
        if form == "JSON":
            return text
        names = ["blockHash", "blockNumber", "from", "gas", "gasPrice", "input", "nonce", "to",
                 "transactionIndex", "value", "contractAddress", "cumulativeGasUsed", "gasUsed", "logs"]
        return [_field(text, name) for name in names]

    def Count_Outgoing_XDC_Transactions(API_KEY, Address, form="JSON", conn=None):
        return _request("GET", "/v3/xdc/transaction/count/%s" % _path(Address), API_KEY, conn=conn)

    def Send_XDC_ERC20(API_KEY, To, Amount, FromPrivateKey, Data=None, Nonce=None, Fee=None, form="JSON", conn=None):
        """Sends real funds, and hands FromPrivateKey to Tatum. Only use it with a throwaway test key."""
        payload = {
            "to": API.required("To", To),
            "amount": str(API.required("Amount", Amount)),
            "fromPrivateKey": API.required("FromPrivateKey", FromPrivateKey),
        }
        if Data is not None:
            payload["data"] = Data
        if Nonce is not None:
            payload["nonce"] = Nonce
        if Fee is not None:
            payload["fee"] = Fee
        return _request("POST", "/v3/xdc/transaction", API_KEY, payload, conn)

    def Estimate_XDC_Transaction_Fees(API_KEY, Address1, Address2, Amount, Data=None, form="JSON", conn=None):
        payload = {
            "from": API.required("Address1", Address1),
            "to": API.required("Address2", Address2),
            "amount": str(API.required("Amount", Amount)),
        }
        if Data is not None:
            payload["data"] = Data
        return _request("POST", "/v3/xdc/gas", API_KEY, payload, conn)

    def Execute_Smart_Contract(API_KEY, contractAddress, methodName, methodABI, params, FromPrivateKey=None, Fee=None, form="JSON", conn=None):
        """A call that changes state needs FromPrivateKey, which goes to Tatum. Only use a throwaway test key."""
        payload = {
            "contractAddress": API.required("contractAddress", contractAddress),
            "methodName": API.required("methodName", methodName),
            "methodABI": API.required("methodABI", methodABI),
            "params": params,
        }
        if FromPrivateKey is not None:
            payload["fromPrivateKey"] = FromPrivateKey
        if Fee is not None:
            payload["fee"] = Fee
        return _request("POST", "/v3/xdc/smartcontract", API_KEY, payload, conn)

    def Broadcast_Signed_XDC_Transaction(API_KEY, txData, signatureId=None, form="JSON", conn=None):
        payload = {"txData": API.required("txData", txData)}
        if signatureId is not None:
            payload["signatureId"] = signatureId
        return _request("POST", "/v3/xdc/broadcast", API_KEY, payload, conn)
