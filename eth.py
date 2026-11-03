from Base_API_Call import API


class eth_Request:
    def protocolVersion(conn=None, form="JSON"):
        return API.Format("eth_protocolVersion", [], conn, form, id=67)

    def syncing(conn=None, form="JSON"):
        return API.Format("eth_syncing", [], conn, form)

    def coinbase(conn=None, form="JSON"):
        return API.Format("eth_coinbase", [], conn, form, id=64)

    def gasPrice(conn=None, form="JSON"):
        return API.Format("eth_gasPrice", [], conn, form, id=73)

    def accounts(conn=None, form="JSON"):
        return API.Format("eth_accounts", [], conn, form)

    def blockNumber(conn=None, form="JSON"):
        return API.Format("eth_blockNumber", [], conn, form, id=83)

    def getBalance(conn=None, form="JSON", Address="", Block="latest"):
        API.required("Address", Address)
        return API.Format("eth_getBalance", [Address, API.quantity(Block)], conn, form)

    def getStorageAt(conn=None, form="JSON", Address="", Position="", Block="latest"):
        API.required("Address", Address)
        API.required("Position", Position)
        return API.Format("eth_getStorageAt", [Address, API.quantity(Position), API.quantity(Block)], conn, form)

    def getTransactionCount(conn=None, form="JSON", Address="", Block="latest"):
        API.required("Address", Address)
        return API.Format("eth_getTransactionCount", [Address, API.quantity(Block)], conn, form)

    def getBlockTransactionCountByHash(conn=None, form="JSON", Hash=""):
        API.required("Hash", Hash)
        return API.Format("eth_getBlockTransactionCountByHash", [Hash], conn, form)

    def getBlockTransactionCountByNumber(conn=None, form="JSON", Block=""):
        API.required("Block", Block)
        return API.Format("eth_getBlockTransactionCountByNumber", [API.quantity(Block)], conn, form)

    def getCode(conn=None, form="JSON", Address="", Block="latest"):
        API.required("Address", Address)
        return API.Format("eth_getCode", [Address, API.quantity(Block)], conn, form)

    def sign(conn=None, form="JSON", Address="", Data=""):
        """Asks the node to sign with an account it holds. Public nodes hold no accounts and refuse."""
        API.required("Address", Address)
        API.required("Data", Data)
        return API.Format("eth_sign", [Address, Data], conn, form)

    def sendTransaction(conn=None, form="JSON", Transaction=None):
        """Asks the node to sign and send. Public nodes hold no accounts and refuse."""
        API.required("Transaction", Transaction)
        return API.Format("eth_sendTransaction", [Transaction], conn, form)

    def sendRawTransaction(conn=None, form="JSON", Data=""):
        API.required("Data", Data)
        return API.Format("eth_sendRawTransaction", [Data], conn, form)

    def call(conn=None, form="JSON", Transaction=None, Block="latest"):
        API.required("Transaction", Transaction)
        return API.Format("eth_call", [Transaction, API.quantity(Block)], conn, form)

    def estimateGas(conn=None, form="JSON", Transaction=None):
        API.required("Transaction", Transaction)
        return API.Format("eth_estimateGas", [Transaction], conn, form)

    def getBlockByHash(conn=None, form="JSON", Hash="", Full=True):
        API.required("Hash", Hash)
        return API.Format("eth_getBlockByHash", [Hash, Full], conn, form)

    def getBlockByNumber(conn=None, form="JSON", Block="latest", Full=True):
        return API.Format("eth_getBlockByNumber", [API.quantity(Block), Full], conn, form)

    def getBlockSignersByNumber(conn=None, form="JSON", Block=""):
        API.required("Block", Block)
        return API.Format("eth_getBlockSignersByNumber", [API.quantity(Block)], conn, form)

    def getBlockSignersByHash(conn=None, form="JSON", Hash=""):
        API.required("Hash", Hash)
        return API.Format("eth_getBlockSignersByHash", [Hash], conn, form)

    def getBlockFinalityByNumber(conn=None, form="JSON", Block=""):
        API.required("Block", Block)
        return API.Format("eth_getBlockFinalityByNumber", [API.quantity(Block)], conn, form)

    def getBlockFinalityByHash(conn=None, form="JSON", Hash=""):
        API.required("Hash", Hash)
        return API.Format("eth_getBlockFinalityByHash", [Hash], conn, form)

    def getCandidates(conn=None, form="JSON", Epoch="latest"):
        return API.Format("eth_getCandidates", [API.quantity(Epoch)], conn, form)

    def getCandidateStatus(conn=None, form="JSON", Candidate="", Epoch="latest"):
        API.required("Candidate", Candidate)
        return API.Format("eth_getCandidateStatus", [Candidate, API.quantity(Epoch)], conn, form)

    def getTransactionByHash(conn=None, form="JSON", Hash=""):
        API.required("Hash", Hash)
        return API.Format("eth_getTransactionByHash", [Hash], conn, form)

    def getTransactionByBlockHashAndIndex(conn=None, form="JSON", Hash="", Index=0):
        API.required("Hash", Hash)
        return API.Format("eth_getTransactionByBlockHashAndIndex", [Hash, API.quantity(Index)], conn, form)

    def getTransactionByBlockNumberAndIndex(conn=None, form="JSON", Block="", Index=0):
        API.required("Block", Block)
        return API.Format("eth_getTransactionByBlockNumberAndIndex", [API.quantity(Block), API.quantity(Index)], conn, form)

    def getTransactionReceipt(conn=None, form="JSON", Hash=""):
        API.required("Hash", Hash)
        return API.Format("eth_getTransactionReceipt", [Hash], conn, form)
