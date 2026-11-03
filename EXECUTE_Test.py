"""Live, read-only checks against real services. The tests in tests/ need no network.

python3 EXECUTE_Test.py rpc      reads from the public XDC node
python3 EXECUTE_Test.py tatum    reads from Tatum, and needs TATUM_API_KEY and TATUM_ADDRESS

Nothing here sends a transaction or handles a seed or private key.
"""
import os
import sys

from eth import eth_Request
from net import net_Request
from tatum import tatum_Request
from web3 import web3_Request


def rpc_test():
    print("Client version:", web3_Request.clientVersion(form="Text"))
    print("Network:", net_Request.version(form="Text"))
    print("Latest block:", int(eth_Request.blockNumber(form="Text"), 16))
    print("Gas price:", int(eth_Request.gasPrice(form="Text"), 16))


def tatum_test():
    missing = [name for name in ("TATUM_API_KEY", "TATUM_ADDRESS") if not os.environ.get(name)]
    if missing:
        sys.exit("Set %s to run this check" % " and ".join(missing))
    key = os.environ["TATUM_API_KEY"]
    address = os.environ["TATUM_ADDRESS"]
    print("Current block:", tatum_Request.Current_Block_Number(key))
    print("Balance:", tatum_Request.XDC_Account_Balance(key, address, form="Text"))
    print("Outgoing transactions:", tatum_Request.Count_Outgoing_XDC_Transactions(key, address))


if __name__ == "__main__":
    checks = {"rpc": rpc_test, "tatum": tatum_test}
    if len(sys.argv) != 2 or sys.argv[1] not in checks:
        sys.exit(__doc__)
    checks[sys.argv[1]]()
