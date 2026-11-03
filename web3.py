from Base_API_Call import API


class web3_Request:
    def clientVersion(conn=None, form="JSON"):
        return API.Format("web3_clientVersion", [], conn, form, id=67)

    def sha3(conn=None, form="JSON", Hash=""):
        """Hash is the data to hash, as hex, with or without the 0x."""
        API.required("Hash", Hash)
        data = Hash if Hash.startswith("0x") else "0x" + Hash
        return API.Format("web3_sha3", [data], conn, form, id=64)
