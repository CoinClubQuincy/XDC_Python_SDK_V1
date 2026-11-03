import http.client
import json

DEFAULT_HOST = "rpc.xinfin.network"
TIMEOUT = 30
USER_AGENT = "XDC-Python-SDK/1"


class APIError(Exception):
    """A request failed: the server was unreachable, refused it, or sent something unreadable."""


class RPCError(APIError):
    """The node answered with a JSON-RPC error."""

    def __init__(self, code, message):
        super().__init__("RPC error %s: %s" % (code, message))
        self.code = code
        self.message = message


class API:
    def Connect(host=DEFAULT_HOST):
        return http.client.HTTPSConnection(host, timeout=TIMEOUT)

    def Call(call, payload, content, conn, headers=None):
        """Sends one request and returns the body as text. Any failure raises APIError."""
        all_headers = {"content-type": "application/json", "user-agent": USER_AGENT}
        if headers:
            all_headers.update(headers)
        try:
            conn.request(call, content, payload, all_headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
        except (OSError, http.client.HTTPException, UnicodeDecodeError) as error:
            conn.close()
            raise APIError("Request failed: %s" % error) from error
        if res.status >= 400:
            raise APIError("Server returned HTTP %s: %s" % (res.status, data[:200]))
        return data

    def Request_formatter(text):
        """Returns the result of a JSON-RPC response. An error response raises RPCError."""
        try:
            item = json.loads(text)
        except ValueError as error:
            raise APIError("Response was not JSON: %s" % text[:200]) from error
        if not isinstance(item, dict):
            raise APIError("Unexpected response: %s" % text[:200])
        if item.get("error"):
            error = item["error"]
            raise RPCError(error.get("code"), error.get("message"))
        if "result" not in item:
            raise APIError("Response has no result: %s" % text[:200])
        return item["result"]

    def Format(method, params, conn=None, form="JSON", id=1, content="/"):
        """Calls a JSON-RPC method. form="JSON" returns the raw response, anything else the result."""
        payload = json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": id})
        own_connection = conn is None
        if own_connection:
            conn = API.Connect()
        try:
            text = API.Call("POST", payload, content, conn)
        finally:
            if own_connection:
                conn.close()
        if form == "JSON":
            return text
        return API.Request_formatter(text)

    def required(name, value):
        """Refuses an empty input, so a call never goes out with a value the caller didn't choose."""
        if value is None or value == "" or value == {}:
            raise ValueError("%s is required" % name)
        return value

    def quantity(value):
        """Turns a whole number into the hex string JSON-RPC expects. Strings pass through unchanged."""
        if isinstance(value, bool):
            raise ValueError("Expected a number or a hex string")
        return hex(value) if isinstance(value, int) else value
