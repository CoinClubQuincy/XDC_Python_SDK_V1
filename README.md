# XDC3PYTHON
```
XDC3PYTHON SDK with support for smart contracts, XRC20 & XRC721.
```

# Usage
```
run this command pip install XDC3PYTHON to add dependecies.
```

[dependencies]
```
XDC3PYTHON = "1.0.0"
```

This SDK supports following Read & Write operations:-


```

  |    XRC20 Token: Read methods                            |   XRC20 Token: Write methods                          |
  |                                                         |                                                       | 
  |     name()                                              |   approve(receiverAddress , amount)                   |
  |     symbol()                                            |   transfer(recipient, amount)                         |
  |     decimal()                                           |   transferFrom(sender, recipient, amount)             |
  |     totalSupply()                                       |   increaseAllowance(spender, addedValue)              |
  |     balanceOf(account)                                  |   decreaseAllowance(spender, subtractedValue)         |
  |     allowance(owner, spender)                           |                                                       |
  |                                                         |                                                       |
                                            
  |    XRC721 Token: Read methods                           |   XRC721 Token: Write methods                         |
  |                                                         |                                                       |
  |     name()                                              |   setApprovalForAll(spenderAddress, booleanValue)     |
  |     symbol()                                            |   approve(spenderAddress , tokenId)                   |
  |     totalSupply()                                       |   transferFrom(receiver, tokenId)                     |
  |     balanceOf(ownerAddress)                             |   safeTransferFrom(receiver, tokenId)                 |
  |     ownerOf(tokenId)                                    |                                                       |
  |     tokenURI(tokenId)                                   |                                                       |
  |     tokenByIndex(index)                                 |                                                       |
  |     tokenOfOwnerByIndex(ownerAddress,index)             |                                                       |
  |     supportInterface(interfaceId)                       |                                                       |
  |     getApproved(tokenId)                                |                                                       |
  |     isApprovedForAll(ownerAddress,spenderAddr)          |                                                       |
  |                                                         |                                                       |

```

# Environment Variable
```
Create a .env file in the root directory of the Python project to put the wallet and endpoint information in like so: NETWORK_URL = "https://rpc.apothem.network"
```

Example for XRC20.
```

from XDC3PYTHON import XRC20


if __name__=="__main__":

    token = input('Enter token address: ')
    a = XRC20.name(token)
    print(a)
```

This example returns name of the specified address.

Example for XRC721.
```

from XDC3PYTHON import XRC721


if __name__=="__main__":

    token = input('Enter token address: ')
    a = XRC721.symbol(token)
    print(a)
```

This example returns symbol of the specified address.

# Transports
```
 HTTP transport
```
