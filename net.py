from Base_API_Call import API


class net_Request:
    def version(conn=None, form="JSON"):
        return API.Format("net_version", [], conn, form, id=67)

    def listening(conn=None, form="JSON"):
        return API.Format("net_listening", [], conn, form, id=67)

    def peerCount(conn=None, form="JSON"):
        return API.Format("net_peerCount", [], conn, form, id=74)
