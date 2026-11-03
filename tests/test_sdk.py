"""Tests against a local mock server. They make no outside network calls."""
import http.client
import http.server
import inspect
import json
import os
import re
import subprocess
import sys
import threading
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from Base_API_Call import API, APIError, RPCError, TIMEOUT  # noqa: E402
from eth import eth_Request  # noqa: E402
from net import net_Request  # noqa: E402
from tatum import tatum_Request  # noqa: E402
from web3 import web3_Request  # noqa: E402

ADDRESS = "0x" + "a1" * 20
HASH = "0x" + "b2" * 32
TX = {"from": ADDRESS, "to": "0x" + "c3" * 20, "value": "0x1"}


class Handler(http.server.BaseHTTPRequestHandler):
    def respond(self):
        length = int(self.headers.get("content-length") or 0)
        body = self.rfile.read(length).decode() if length else None
        self.server.requests.append({"method": self.command, "path": self.path, "headers": self.headers, "body": body})
        self.send_response(self.server.status)
        reply = self.server.reply.encode()
        self.send_header("content-length", str(len(reply)))
        self.end_headers()
        self.wfile.write(reply)

    do_GET = respond
    do_POST = respond

    def log_message(self, *args):
        pass


class ServerTest(unittest.TestCase):
    def setUp(self):
        self.server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
        self.server.requests = []
        self.server.status = 200
        self.server.reply = json.dumps({"jsonrpc": "2.0", "id": 1, "result": "0x10"})
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.conn = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=5)
        self.addCleanup(self.conn.close)

    def last(self):
        return self.server.requests[-1]

    def sent(self):
        return json.loads(self.last()["body"])


class RpcMethodsTest(ServerTest):
    def assert_sends(self, function, method, params, **inputs):
        function(conn=self.conn, **inputs)
        request = self.sent()
        self.assertEqual(request["method"], method)
        self.assertEqual(request["params"], params)
        self.assertEqual(request["jsonrpc"], "2.0")

    def test_every_eth_method_sends_what_it_was_given(self):
        E = eth_Request
        cases = [
            (E.protocolVersion, "eth_protocolVersion", [], {}),
            (E.syncing, "eth_syncing", [], {}),
            (E.coinbase, "eth_coinbase", [], {}),
            (E.gasPrice, "eth_gasPrice", [], {}),
            (E.accounts, "eth_accounts", [], {}),
            (E.blockNumber, "eth_blockNumber", [], {}),
            (E.getBalance, "eth_getBalance", [ADDRESS, "latest"], {"Address": ADDRESS}),
            (E.getStorageAt, "eth_getStorageAt", [ADDRESS, "0x2", "0x5"], {"Address": ADDRESS, "Position": 2, "Block": 5}),
            (E.getTransactionCount, "eth_getTransactionCount", [ADDRESS, "latest"], {"Address": ADDRESS}),
            (E.getBlockTransactionCountByHash, "eth_getBlockTransactionCountByHash", [HASH], {"Hash": HASH}),
            (E.getBlockTransactionCountByNumber, "eth_getBlockTransactionCountByNumber", ["0xa"], {"Block": 10}),
            (E.getCode, "eth_getCode", [ADDRESS, "latest"], {"Address": ADDRESS}),
            (E.sign, "eth_sign", [ADDRESS, "0xabcd"], {"Address": ADDRESS, "Data": "0xabcd"}),
            (E.sendTransaction, "eth_sendTransaction", [TX], {"Transaction": TX}),
            (E.sendRawTransaction, "eth_sendRawTransaction", ["0xabcd"], {"Data": "0xabcd"}),
            (E.call, "eth_call", [TX, "latest"], {"Transaction": TX}),
            (E.estimateGas, "eth_estimateGas", [TX], {"Transaction": TX}),
            (E.getBlockByHash, "eth_getBlockByHash", [HASH, False], {"Hash": HASH, "Full": False}),
            (E.getBlockByNumber, "eth_getBlockByNumber", ["latest", True], {}),
            (E.getBlockSignersByNumber, "eth_getBlockSignersByNumber", ["0xa"], {"Block": 10}),
            (E.getBlockSignersByHash, "eth_getBlockSignersByHash", [HASH], {"Hash": HASH}),
            (E.getBlockFinalityByNumber, "eth_getBlockFinalityByNumber", ["0xa"], {"Block": 10}),
            (E.getBlockFinalityByHash, "eth_getBlockFinalityByHash", [HASH], {"Hash": HASH}),
            (E.getCandidates, "eth_getCandidates", ["latest"], {}),
            (E.getCandidateStatus, "eth_getCandidateStatus", [ADDRESS, "latest"], {"Candidate": ADDRESS}),
            (E.getTransactionByHash, "eth_getTransactionByHash", [HASH], {"Hash": HASH}),
            (E.getTransactionByBlockHashAndIndex, "eth_getTransactionByBlockHashAndIndex", [HASH, "0x1"], {"Hash": HASH, "Index": 1}),
            (E.getTransactionByBlockNumberAndIndex, "eth_getTransactionByBlockNumberAndIndex", ["0xa", "0x1"], {"Block": 10, "Index": 1}),
            (E.getTransactionReceipt, "eth_getTransactionReceipt", [HASH], {"Hash": HASH}),
        ]
        methods = [name for name, value in vars(eth_Request).items() if inspect.isfunction(value)]
        self.assertEqual(len(cases), len(methods))
        for function, method, params, inputs in cases:
            with self.subTest(method=method):
                self.assert_sends(function, method, params, **inputs)

    def test_required_inputs_are_refused_before_anything_is_sent(self):
        E = eth_Request
        cases = [
            (E.getBalance, {}), (E.getStorageAt, {"Address": ADDRESS}), (E.getTransactionCount, {}),
            (E.getBlockTransactionCountByHash, {}), (E.getBlockTransactionCountByNumber, {}), (E.getCode, {}),
            (E.sign, {"Address": ADDRESS}), (E.sendTransaction, {}), (E.sendRawTransaction, {}), (E.call, {}),
            (E.estimateGas, {}), (E.getBlockByHash, {}), (E.getBlockSignersByNumber, {}), (E.getBlockSignersByHash, {}),
            (E.getBlockFinalityByNumber, {}), (E.getBlockFinalityByHash, {}), (E.getCandidateStatus, {}),
            (E.getTransactionByHash, {}), (E.getTransactionByBlockHashAndIndex, {}),
            (E.getTransactionByBlockNumberAndIndex, {}), (E.getTransactionReceipt, {}), (web3_Request.sha3, {}),
        ]
        for function, inputs in cases:
            with self.subTest(function=function.__name__):
                with self.assertRaises(ValueError):
                    function(conn=self.conn, **inputs)
        self.assertEqual(self.server.requests, [])

    def test_sources_hold_no_sample_addresses_or_hashes(self):
        for name in ("eth.py", "net.py", "web3.py", "tatum.py"):
            with open(os.path.join(ROOT, name)) as source:
                self.assertIsNone(re.search(r"(0x|xdc)[0-9a-fA-F]{40,}", source.read()), name)

    def test_web3_and_net_methods(self):
        self.assert_sends(web3_Request.clientVersion, "web3_clientVersion", [])
        self.assert_sends(web3_Request.sha3, "web3_sha3", ["0xabcd"], Hash="abcd")
        self.assert_sends(web3_Request.sha3, "web3_sha3", ["0xabcd"], Hash="0xabcd")
        self.assert_sends(net_Request.version, "net_version", [])
        self.assert_sends(net_Request.listening, "net_listening", [])
        self.assert_sends(net_Request.peerCount, "net_peerCount", [])

    def test_requests_go_to_the_root_path(self):
        net_Request.version(conn=self.conn)
        self.assertEqual(self.last()["path"], "/")

    def test_requests_identify_the_sdk(self):
        net_Request.version(conn=self.conn)
        self.assertEqual(self.last()["headers"]["user-agent"], "XDC-Python-SDK/1")


class ResponsesTest(ServerTest):
    def test_json_form_returns_the_raw_response(self):
        self.assertEqual(json.loads(net_Request.version(conn=self.conn))["result"], "0x10")

    def test_text_form_returns_the_result(self):
        self.assertEqual(net_Request.version(conn=self.conn, form="Text"), "0x10")

    def test_rpc_errors_are_raised_with_their_code(self):
        self.server.reply = json.dumps({"jsonrpc": "2.0", "id": 1, "error": {"code": -32601, "message": "not found"}})
        with self.assertRaises(RPCError) as caught:
            net_Request.version(conn=self.conn, form="Text")
        self.assertEqual(caught.exception.code, -32601)
        self.assertIn("not found", str(caught.exception))

    def test_rpc_errors_are_raised_in_the_json_form_too(self):
        self.server.reply = json.dumps({"jsonrpc": "2.0", "id": 1, "error": {"code": -32601, "message": "not found"}})
        with self.assertRaises(RPCError):
            net_Request.version(conn=self.conn)

    def test_an_error_that_is_not_an_object_is_still_an_error(self):
        self.server.reply = json.dumps({"jsonrpc": "2.0", "id": 1, "error": "busy"})
        with self.assertRaises(APIError):
            net_Request.version(conn=self.conn, form="Text")

    def test_a_false_result_is_still_a_result(self):
        self.server.reply = json.dumps({"jsonrpc": "2.0", "id": 1, "result": False})
        self.assertIs(eth_Request.syncing(conn=self.conn, form="Text"), False)

    def test_null_result_is_still_a_result(self):
        self.server.reply = json.dumps({"jsonrpc": "2.0", "id": 1, "result": None})
        self.assertIsNone(eth_Request.getTransactionReceipt(conn=self.conn, form="Text", Hash=HASH))

    def test_unreadable_responses_are_raised(self):
        for reply in ("<html>bad gateway</html>", "[]", "{}"):
            for form in ("JSON", "Text"):
                with self.subTest(reply=reply, form=form):
                    self.server.reply = reply
                    with self.assertRaises(APIError):
                        net_Request.version(conn=self.conn, form=form)

    def test_http_errors_are_raised_in_both_forms(self):
        self.server.status = 502
        self.server.reply = "bad gateway"
        for form in ("JSON", "Text"):
            with self.subTest(form=form):
                with self.assertRaises(APIError) as caught:
                    net_Request.version(conn=self.conn, form=form)
                self.assertIn("502", str(caught.exception))

    def test_redirects_are_errors(self):
        self.server.status = 302
        self.server.reply = "moved"
        with self.assertRaises(APIError) as caught:
            net_Request.version(conn=self.conn)
        self.assertIn("302", str(caught.exception))

    def test_connection_failures_are_raised(self):
        port = self.server.server_port
        self.server.shutdown()
        self.server.server_close()
        closed = http.client.HTTPConnection("127.0.0.1", port, timeout=1)
        with self.assertRaises(APIError):
            net_Request.version(conn=closed)


class ConnectionsTest(unittest.TestCase):
    def test_nothing_connects_at_import_time(self):
        for cls in (eth_Request, net_Request, web3_Request):
            for name, function in vars(cls).items():
                if inspect.isfunction(function):
                    self.assertIsNone(inspect.signature(function).parameters["conn"].default, name)

    def test_connections_have_a_timeout(self):
        self.assertEqual(API.Connect().timeout, TIMEOUT)
        self.assertEqual(API.Connect().host, "rpc.xinfin.network")

    def test_an_own_connection_is_closed_even_on_failure(self):
        fake = mock.Mock()
        fake.request.side_effect = OSError("down")
        with mock.patch.object(API, "Connect", return_value=fake):
            with self.assertRaises(APIError):
                net_Request.version()
        fake.close.assert_called()

    def test_a_callers_connection_stays_open(self):
        fake = mock.Mock()
        fake.getresponse.return_value = mock.Mock(status=200, read=lambda: b'{"result":"0x1"}')
        net_Request.version(conn=fake, form="Text")
        fake.close.assert_not_called()

    def test_quantity(self):
        self.assertEqual(API.quantity(255), "0xff")
        self.assertEqual(API.quantity("latest"), "latest")
        with self.assertRaises(ValueError):
            API.quantity(True)


class TatumTest(ServerTest):
    KEY = "test-api-key"

    def test_wallet_encodes_the_seed_and_sends_the_key_as_a_header(self):
        tatum_Request.Generate_XDC_Wallet("one two three", self.KEY, conn=self.conn)
        request = self.last()
        self.assertEqual(request["path"], "/v3/xdc/wallet?mnemonic=one%20two%20three")
        self.assertEqual(request["headers"]["x-api-key"], self.KEY)

    def test_text_forms_return_their_field(self):
        cases = [
            (lambda: tatum_Request.Generate_XDC_Wallet("seed", self.KEY, form="Text", conn=self.conn), "xpub"),
            (lambda: tatum_Request.Generate_XDC_Wallet_EPK(self.KEY, "pub", 0, form="Text", conn=self.conn), "address"),
            (lambda: tatum_Request.Generate_XDC_Private_key(self.KEY, "seed", form="Text", conn=self.conn), "key"),
            (lambda: tatum_Request.XDC_Account_Balance(self.KEY, ADDRESS, form="Text", conn=self.conn), "balance"),
        ]
        for call, field in cases:
            with self.subTest(field=field):
                self.server.reply = json.dumps({field: "value"})
                self.assertEqual(call(), "value")
                self.server.reply = "{}"
                with self.assertRaises(APIError):
                    call()

    def test_get_paths(self):
        cases = [
            (lambda: tatum_Request.Generate_XDC_Wallet_EPK(self.KEY, "pub", 3, conn=self.conn), "/v3/xdc/address/pub/3"),
            (lambda: tatum_Request.Current_Block_Number(self.KEY, conn=self.conn), "/v3/xdc/block/current"),
            (lambda: tatum_Request.XDC_Block_by_Hash(self.KEY, "abc", conn=self.conn), "/v3/xdc/block/abc"),
            (lambda: tatum_Request.XDC_Account_Balance(self.KEY, "abc", conn=self.conn), "/v3/xdc/account/balance/abc"),
            (lambda: tatum_Request.XDC_Transaction(self.KEY, "abc", conn=self.conn), "/v3/xdc/transaction/abc"),
            (lambda: tatum_Request.Count_Outgoing_XDC_Transactions(self.KEY, "abc", conn=self.conn), "/v3/xdc/transaction/count/abc"),
        ]
        for call, path in cases:
            with self.subTest(path=path):
                call()
                self.assertEqual(self.last()["path"], path)
                self.assertEqual(self.last()["method"], "GET")

    def test_path_values_cannot_change_the_url(self):
        tatum_Request.XDC_Block_by_Hash(self.KEY, "../../admin?x=1", conn=self.conn)
        self.assertEqual(self.last()["path"], "/v3/xdc/block/..%2F..%2Fadmin%3Fx%3D1")

    def test_dot_paths_are_refused(self):
        for value in (".", ".."):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    tatum_Request.XDC_Block_by_Hash(self.KEY, value, conn=self.conn)
        self.assertEqual(self.server.requests, [])

    def test_transaction_text_form_returns_every_field(self):
        names = ["blockHash", "blockNumber", "from", "gas", "gasPrice", "input", "nonce", "to",
                 "transactionIndex", "value", "contractAddress", "cumulativeGasUsed", "gasUsed", "logs"]
        self.server.reply = json.dumps({name: name for name in names})
        self.assertEqual(tatum_Request.XDC_Transaction(self.KEY, HASH, form="Text", conn=self.conn), names)

    def test_send_uses_only_what_it_was_given(self):
        tatum_Request.Send_XDC_ERC20(self.KEY, "to-address", 5, "test-signing-key", conn=self.conn)
        self.assertEqual(self.last()["path"], "/v3/xdc/transaction")
        self.assertEqual(self.sent(), {"to": "to-address", "amount": "5", "fromPrivateKey": "test-signing-key"})

    def test_send_passes_optional_fields(self):
        fee = {"gasLimit": "40000", "gasPrice": "20"}
        tatum_Request.Send_XDC_ERC20(self.KEY, "a", 1, "k", Data="note", Nonce=0, Fee=fee, conn=self.conn)
        self.assertEqual(self.sent()["data"], "note")
        self.assertEqual(self.sent()["nonce"], 0)
        self.assertEqual(self.sent()["fee"], fee)

    def test_send_needs_all_its_inputs(self):
        for inputs in (("", 1, "k"), ("a", "", "k"), ("a", 1, "")):
            with self.subTest(inputs=inputs):
                with self.assertRaises(ValueError):
                    tatum_Request.Send_XDC_ERC20(self.KEY, *inputs, conn=self.conn)
        self.assertEqual(self.server.requests, [])

    def test_estimate_uses_what_it_was_given(self):
        tatum_Request.Estimate_XDC_Transaction_Fees(self.KEY, "a", "b", 7, conn=self.conn)
        self.assertEqual(self.last()["path"], "/v3/xdc/gas")
        self.assertEqual(self.sent(), {"from": "a", "to": "b", "amount": "7"})

    def test_contract_call_uses_what_it_was_given(self):
        abi = {"name": "stake", "type": "function"}
        tatum_Request.Execute_Smart_Contract(self.KEY, "c", "stake", abi, ["1"], conn=self.conn)
        self.assertEqual(self.last()["path"], "/v3/xdc/smartcontract")
        self.assertEqual(self.sent(), {"contractAddress": "c", "methodName": "stake", "methodABI": abi, "params": ["1"]})

    def test_broadcast_uses_what_it_was_given(self):
        tatum_Request.Broadcast_Signed_XDC_Transaction(self.KEY, "0xabc", conn=self.conn)
        self.assertEqual(self.last()["path"], "/v3/xdc/broadcast")
        self.assertEqual(self.sent(), {"txData": "0xabc"})

    def test_private_key_request_sends_the_seed_in_the_body(self):
        tatum_Request.Generate_XDC_Private_key(self.KEY, "my seed", conn=self.conn)
        self.assertEqual(self.last()["path"], "/v3/xdc/wallet/priv")
        self.assertEqual(self.sent(), {"index": 0, "mnemonic": "my seed"})

    def test_web3_driver(self):
        tatum_Request.Web3_HTTP_Driver(self.KEY, conn=self.conn)
        self.assertEqual(self.last()["path"], "/v3/xdc/web3/test-api-key")
        self.assertEqual(self.sent()["method"], "web3_clientVersion")

    def test_the_api_key_never_appears_in_an_error(self):
        self.server.status = 401
        self.server.reply = "unauthorized"
        with self.assertRaises(APIError) as caught:
            tatum_Request.Current_Block_Number(self.KEY, conn=self.conn)
        self.assertNotIn(self.KEY, str(caught.exception))

    def test_a_bad_api_key_is_not_echoed(self):
        secret = "secret\nvalue"
        with self.assertRaises(ValueError) as caught:
            tatum_Request.Current_Block_Number(secret, conn=self.conn)
        self.assertNotIn("secret", str(caught.exception))
        self.assertEqual(self.server.requests, [])

    def test_a_rejected_header_is_not_echoed(self):
        with self.assertRaises(APIError) as caught:
            API.Call("GET", None, "/", self.conn, headers={"x-api-key": "secret\nvalue"})
        self.assertNotIn("secret", str(caught.exception))
        self.assertTrue(caught.exception.__suppress_context__)
        self.assertEqual(self.server.requests, [])

    def test_a_missing_api_key_is_refused(self):
        with self.assertRaises(ValueError):
            tatum_Request.Current_Block_Number("", conn=self.conn)
        self.assertEqual(self.server.requests, [])


class LiveCheckScriptTest(unittest.TestCase):
    def run_script(self, *args):
        env = {key: value for key, value in os.environ.items() if not key.startswith("TATUM_")}
        return subprocess.run([sys.executable, "EXECUTE_Test.py", *args], cwd=ROOT, env=env, capture_output=True, text=True, timeout=30)

    def test_needs_a_choice(self):
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("rpc", result.stderr)

    def test_tatum_check_says_what_is_missing(self):
        result = self.run_script("tatum")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("TATUM_API_KEY", result.stderr)
        self.assertIn("TATUM_ADDRESS", result.stderr)

    def test_script_never_touches_seeds_or_private_keys(self):
        with open(os.path.join(ROOT, "EXECUTE_Test.py")) as source:
            code = source.read()
        self.assertNotIn("Generate_XDC_Private_key", code)
        self.assertNotIn("TATUM_SEED", code)


if __name__ == "__main__":
    unittest.main()
