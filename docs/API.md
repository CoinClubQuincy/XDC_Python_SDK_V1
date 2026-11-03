# API reference

Every method also takes `form` and `conn`.

| Argument | Default | Meaning |
| --- | --- | --- |
| `form` | `"JSON"` | `"JSON"` returns the raw response text. `"Text"` returns the value of the result |
| `conn` | `None` | An open `http.client` connection to reuse. By default each call opens and closes its own |

RPC calls go to `rpc.xinfin.network`, and Tatum calls go to `api-eu1.tatum.io`.

Block numbers, positions and indexes can be integers, which are converted to hex, or strings such as `"latest"`. Inputs with no default are required, and a missing one raises `ValueError` before anything is sent.

## Errors

| Exception | When |
| --- | --- |
| `ValueError` | A required input is missing, an API key has a control character, or a value placed in a URL is `.` or `..` |
| `RPCError` | The node refused the call, in either form. It has `code` and `message` |
| `APIError` | The connection failed, the server returned anything other than a 2xx status, or the reply could not be read |

## web3

| Call | Returns |
| --- | --- |
| `web3_Request.clientVersion()` | Node software version |
| `web3_Request.sha3(Hash=data)` | Keccak-256 of hex data. `0x` is added if it is missing |

## net

| Call | Returns |
| --- | --- |
| `net_Request.version()` | Network ID |
| `net_Request.listening()` | Whether the node accepts connections |
| `net_Request.peerCount()` | Number of peers, as hex |

## eth

Inputs are keyword arguments, for example `eth_Request.getBalance(Address="0x...")`. Each one sends the JSON-RPC method `eth_<name>`. `Transaction` is a dictionary such as `{"from": ..., "to": ..., "value": "0x1"}`.

| Method | Inputs | Returns |
| --- | --- | --- |
| `protocolVersion` |  | Protocol version |
| `syncing` |  | Sync state, or false |
| `coinbase` |  | Node's coinbase address |
| `gasPrice` |  | Gas price in wei, as hex |
| `accounts` |  | Accounts the node holds |
| `blockNumber` |  | Latest block number, as hex |
| `getBalance` | `Address, Block="latest"` | Balance in wei, as hex |
| `getStorageAt` | `Address, Position, Block="latest"` | A storage slot |
| `getTransactionCount` | `Address, Block="latest"` | Nonce of an address |
| `getBlockTransactionCountByHash` | `Hash` | Transactions in a block |
| `getBlockTransactionCountByNumber` | `Block` | Transactions in a block |
| `getCode` | `Address, Block="latest"` | Contract bytecode |
| `sign` | `Address, Data` | Signs with an account the node holds |
| `sendTransaction` | `Transaction` | Sends with an account the node holds |
| `sendRawTransaction` | `Data` | Sends a transaction you signed |
| `call` | `Transaction, Block="latest"` | Read-only contract call |
| `estimateGas` | `Transaction` | Gas estimate |
| `getBlockByHash` | `Hash, Full=True` | A block. `Full` includes whole transactions |
| `getBlockByNumber` | `Block="latest", Full=True` | A block |
| `getBlockSignersByNumber` | `Block` | XDPoS block signers |
| `getBlockSignersByHash` | `Hash` | XDPoS block signers |
| `getBlockFinalityByNumber` | `Block` | XDPoS finality |
| `getBlockFinalityByHash` | `Hash` | XDPoS finality |
| `getCandidates` | `Epoch="latest"` | XDPoS masternode candidates |
| `getCandidateStatus` | `Candidate, Epoch="latest"` | XDPoS candidate status |
| `getTransactionByHash` | `Hash` | A transaction |
| `getTransactionByBlockHashAndIndex` | `Hash, Index=0` | A transaction by position |
| `getTransactionByBlockNumberAndIndex` | `Block, Index=0` | A transaction by position |
| `getTransactionReceipt` | `Hash` | A receipt, or null while pending |

## tatum

Arguments can be positional. API keys go in the `x-api-key` header, except for `Web3_HTTP_Driver`. Values placed in a URL are encoded, and `.` and `..` are refused, so they can't change the path.

| Method | Arguments | Request | `form="Text"` returns | Note |
| --- | --- | --- | --- | --- |
| `Generate_XDC_Wallet` | `Seed, API_KEY` | `GET /v3/xdc/wallet` | `xpub` | Sends your seed to Tatum in the URL, so it can end up in logs |
| `Generate_XDC_Wallet_EPK` | `API_KEY, xpub, index` | `GET /v3/xdc/address/{xpub}/{index}` | `address` |  |
| `Generate_XDC_Private_key` | `API_KEY, Seed, index=0` | `POST /v3/xdc/wallet/priv` | `key` | Sends your seed to Tatum |
| `Web3_HTTP_Driver` | `ApiKey` | `POST /v3/xdc/web3/{key}` |  | Puts the key in the URL |
| `Current_Block_Number` | `API_Key` | `GET /v3/xdc/block/current` |  |  |
| `XDC_Block_by_Hash` | `API_KEY, Hash` | `GET /v3/xdc/block/{hash}` |  |  |
| `XDC_Account_Balance` | `API_KEY, Address` | `GET /v3/xdc/account/balance/{address}` | `balance` |  |
| `XDC_Transaction` | `API_KEY, Hash` | `GET /v3/xdc/transaction/{hash}` | List of fields |  |
| `Count_Outgoing_XDC_Transactions` | `API_KEY, Address` | `GET /v3/xdc/transaction/count/{address}` |  |  |
| `Send_XDC_ERC20` | `API_KEY, To, Amount, FromPrivateKey, Data=None, Nonce=None, Fee=None` | `POST /v3/xdc/transaction` |  | Sends your private key to Tatum |
| `Estimate_XDC_Transaction_Fees` | `API_KEY, Address1, Address2, Amount, Data=None` | `POST /v3/xdc/gas` |  |  |
| `Execute_Smart_Contract` | `API_KEY, contractAddress, methodName, methodABI, params, FromPrivateKey=None, Fee=None` | `POST /v3/xdc/smartcontract` |  | Can send your private key to Tatum |
| `Broadcast_Signed_XDC_Transaction` | `API_KEY, txData, signatureId=None` | `POST /v3/xdc/broadcast` |  |  |
