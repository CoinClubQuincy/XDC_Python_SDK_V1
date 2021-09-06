# **XDC Python SDK V1.0**

### **Summary:**

This is a Python SDK for XinFin API published by Quincy@xinfin.org

##### **Haxidecimal Outputs**

All hexadecimal need to be converted into **integers**

##### **JSON Schema**

- By default all functions output in JSON so i implemeted a simplified output for variable just place class(form = "Text")  for vatiabble output as string | Default output "JSON"

- The JSON Schema outputed by all the functions is this:

```json
{
  "jsonrpc":"2.0",
  "id":1,
  "result":EXAMPLE_RESULT
}
```

------



## **web3**

#### **POST /clientVersion**

```python
Version = web3_Request.clientVersion()
print(Version)
##Output {"jsonrpc":"2.0","id":67,"result":"50"}
```

Returns the current client version.

**Parameters**

**form** =  "Text"  for vatiabble output as string | Default output "JSON"

**Returns**

`String` - The current client version

#### **POST /sha3**

```python
import hashlib 
String= "Q"
Hash =  hashlib.sha256(String.encode('utf-8')).hexdigest()

print(web3_Request.sha3(Hash=Hash,form="Text"))
##Output 0x6d1223fcb20bababbf18827dbe3ac76b13f03e2.........
```

Returns Keccak-256 (not the standardized SHA3-256) of the given data.

**Parameters**

​	**form** =  "Text"  for vatiabble output as string | Default output JSON

​	**Hash** - the Hash to convert into a SHA3 hash 

**Returns**`DATA` - The SHA3 result of the given string.

## **net**

#### **POST /version**

```python
Version = net_Request.version(form="Text")
print(Version)
##Output 50
```

Returns the current network id.

**Parameters**

none

**Returns**

- `String` - The current network id.
    - `"50"`: XinFin Mainnet
    - `"89"`: XinFin Testnet

#### **POST /listening**

```python
Listening = net_Request.listening(form="Text")
print(Listening)
##Output True
```

Returns `true` if client is actively listening for network connections.

**Parameters**

none

**Returns**

- `Boolean` - `true` when listening, otherwise `false`.



#### **POST /peerCount**

```python
Peer = net_Request.peerCount(form="Text")
print(Peer)
##Output 0x8
```

Returns number of peers currently connected to the client.

**Parameters**

none

**Returns**

- `QUANTITY` - integer of the number of connected peers.



## **eth**

#### **POST /protocolVersion**

```python
ETH_Version = eth_Request.protocolVersion(form="Text")
print(int(ETH_Version,16)
##Output 63
```

Returns the current ethereum protocol version.

**Parameters**

none

**Returns**

- `String` - The current ethereum protocol version



#### **POST /syncing**

```python
Sync = eth_Request.syncing(form="Text")
print(Sync)
##Output False
```

Returns an object with data about the sync status or false.

**Parameters**

none

**Returns**

- `Object|Boolean`, An object with sync status data or FALSE, when not syncing:
    - `startingBlock`: `QUANTITY` - The block at which the import started (will only be reset, after the sync reached his head)
    - `currentBlock`: `QUANTITY` - The current block, same as eth_blockNumber
    - `highestBlock`: `QUANTITY` - The estimated highest block



#### **POST /coinbase**

```python
coinbase = eth_Request.coinbase(form="Text")
print(coinbase)
##Output xdc3056a8bff9a17b12d08f1837d0b44cf1e2018fbe
```

Returns the client coinbase address. **Parameters** none **Returns**

- `DATA`, 20 bytes - the current coinbase address.



#### **POST /gasPrice**

```python
gasPrice = eth_Request.gasPrice(form="Text")
print(gasPrice)
##Output 0x9c4
```

Returns the current price per gas in wei. **Parameters** none **Returns**

- `QUANTITY` - integer of the current gas price in wei.



#### **POST /accounts**

```
POST /accounts
```

Returns a list of addresses owned by client.

**Parameters**

none

**Returns**

- `Array of DATA`, 20 Bytes - addresses owned by the client



#### **POST /blockNumber**

```
POST /blockNumber
```

Returns the number of most recent block. **Parameters** none **Returns**

- `QUANTITY` - integer of the current block number the client is on.



