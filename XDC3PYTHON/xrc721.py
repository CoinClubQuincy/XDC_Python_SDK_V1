from web3 import Web3
from web3._utils.encoding import (
    hexstr_if_str,
    to_bytes,
)
from decouple import config
import json


rpcUrl = config('NETWORK_URL')

# HTTPProvider:
w3 = Web3(Web3.HTTPProvider(rpcUrl))

# path of abi file
with open('./common/xrc721abi.json') as abiJson:
    xrc721abi = json.load(abiJson)

# This is a class which consists all the methods as per XRC721 standards.

class XRC721:

    # Gets the Name of the specified address.
    # token address required as an argument.

    def name(tokenAddr):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc721abi)
        result = contractInstance.functions.name().call()
        return result

    # Gets the Symbol of the specified address.
    # token address required as an argument.

    def symbol(tokenAddr):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc721abi)
        result = contractInstance.functions.symbol().call()
        return result

    # Gets the owner of an NFT.
    # required arguments.
    # token address, token id.

    def ownerOf(tokenAddr, tokenId):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc721abi)
        result = contractInstance.functions.ownerOf(tokenId).call()
        return result

    # Gets the Totalsupply of the specified address.
    # token address required as an argument.
    
    def totalSupply(tokenAddr):
        token = Web3.toChecksumAddress(tokenAddr)
        contractInstance = w3.eth.contract(address=token, abi=xrc721abi)
        result = contractInstance.functions.totalSupply().call()
        resultt = str(result)
        return resultt

    # Gets the balance of the specified address.
    # reuired arguments
    # token address, owner address.

    def balanceOf(tokenAddr, ownerAddress):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc721abi)
        owner = Web3.toChecksumAddress(ownerAddress)
        result = contractInstance.functions.balanceOf(owner).call()
        return result

    # A distinct Uniform Resource Identifier (URI) for a given asset.
    # Gets URI of a token.
    # required arguments
    # tokenId The identifier for an NFT.
    # address of the token.
    
    def tokenURI(tokenAddr, tokenId):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc721abi)
        result = contractInstance.functions.tokenURI(tokenId).call()
        return result

    # Enumerate NFTs assigned to an owner.
    # tokenAddress An address for whom to query.
    # IndexNO A counter less than `totalSupply()`.
    # The token identifier for the `index`th NFT assigned to `owner`.

    def tokenByIndex(tokenAddr, index):
        token = Web3.toChecksumAddress(tokenAddr)
        contractInstance = w3.eth.contract(address=token, abi=xrc721abi)
        result = contractInstance.functions.tokenByIndex(index).call()
        return result

    # Enumerate NFTs assigned to an owner.
    # The token identifier for the `index`th NFT assigned to `owner`.
    # required arguments.
    # owner address, token address, token index.
    
    def tokenofOwnerByIndex(tokenAddr, ownerAddress, index):
        token = Web3.toChecksumAddress(tokenAddr)
        contractInstance = w3.eth.contract(address=token, abi=xrc721abi)
        owner = Web3.toChecksumAddress(ownerAddress)
        result = contractInstance.functions.tokenOfOwnerByIndex(
            owner, index).call()
        return result

    # Query if a contract implements an interface.
    # tokenAddress An address for whom to query and x_bytes The interface identifier.
    # `true` if the contract implements `interfaceID` andinterfaceID` is not 0xffffffff, `false` otherwise.
    #  required arguments.
    # token address, interface id.

    def supportInterface(tokenAddr, interfaceId):
        token = Web3.toChecksumAddress(tokenAddr)
        contractInstance = w3.eth.contract(address=token, abi=xrc721abi)
        result = contractInstance.functions.supportsInterface(
            interfaceId).call()
        return result

    # The approved address for a token ID, or zero if no address set Reverts if the token ID does not exist.
    # required arguments.
    # token address, tokenId.

    def getApproved(tokenAddr, tokenId):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc721abi)
        result = contractInstance.functions.getApproved(tokenId).call()
        return result

    # Tells whether an operator is approved by a given owner.
    # required arguments.
    # owner address, spender address, token address.

    def isApprovedForAll(tokenAddr, ownerAddress, spenderAddress):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc721abi)
        owner = Web3.toChecksumAddress(ownerAddress)
        spender = Web3.toChecksumAddress(spenderAddress)
        result = contractInstance.functions.isApprovedForAll(
            owner, spender).call()
        return result

    # Change or reaffirm the approved address for an NFT.
    # The zero address indicates there is no approved address.
    # Throws unless `owner` is the current NFT owner, or an authorized.
    # required arguments.
    # tokenAddress, owner address, ownerPrivateKey, spenderAddress, tokenID.

    def approve(tokenAddr, ownerAddress, ownerPrivateKey,  spenderAddress, tokenId):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc721abi)

        owner = Web3.toChecksumAddress(ownerAddress)
        spender = Web3.toChecksumAddress(spenderAddress)

        approveData = contractInstance.functions.approve(spender, tokenId)

        hexData = approveData._encode_transaction_data()

        data = hexstr_if_str(to_bytes, hexData)

        estimateGas = approveData.estimateGas({
            'from': owner,
        })

        nonce = w3.eth.getTransactionCount(owner)

        gasPrice = w3.eth.gas_price

        tx = {
            'nonce': nonce,
            'to': tokenAddr,
            'data': data,
            'gas': estimateGas,
            'gasPrice': gasPrice,
        }

        signedTx = w3.eth.account.signTransaction(tx, ownerPrivateKey)

        txHash = w3.eth.sendRawTransaction(signedTx.rawTransaction)
        return w3.toHex(txHash)

    # Enable or disable approval for a third party ("operator") to manage all of `Owner`'s assets
    # Emits the ApprovalForAll event. The contract MUST allow multiple operators per owner.
    # required arguments.
    # token address, owner address, ownerPrivateKey, sepnder address, tokenId.
     
    def setApprovalForAll(tokenAddr, ownerAddress, ownerPrivateKey,  spenderAddress, boolValue):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc721abi)

        owner = Web3.toChecksumAddress(ownerAddress)
        spender = Web3.toChecksumAddress(spenderAddress)

        approveData = contractInstance.functions.setApprovalForAll(
            spender, boolValue)

        hexData = approveData._encode_transaction_data()

        data = hexstr_if_str(to_bytes, hexData)

        estimateGas = approveData.estimateGas({
            'from': owner,
        })

        nonce = w3.eth.getTransactionCount(owner)

        gasPrice = w3.eth.gas_price

        tx = {
            'nonce': nonce,
            'to': tokenAddr,
            'data': data,
            'gas': estimateGas,
            'gasPrice': gasPrice,
        }

        signedTx = w3.eth.account.signTransaction(tx, ownerPrivateKey)

        txHash = w3.eth.sendRawTransaction(signedTx.rawTransaction)
        return w3.toHex(txHash)

    # Transfer ownership of an NFT -- THE CALLER IS RESPONSIBLE
    # to confirm that `reciever Address` is capable of receiving NFTs or else they may be permanently lost.
    # required arguments.
    # token address, owner address, spender address, spenderPrivateKey, receiver address, tokenId.

    def transferFrom(tokenAddr, ownerAddress, spenderAddress,  spenderPrivateKey, receiver, tokenId):

        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc721abi)

        owner = Web3.toChecksumAddress(ownerAddress)
        receiverAddres = Web3.toChecksumAddress(receiver)
        spender = Web3.toChecksumAddress(spenderAddress)

        transferData = contractInstance.functions.transferFrom(
            owner, receiverAddres, tokenId)

        estimateGas = transferData.estimateGas({
            'from': spender,
        })

        hexData = transferData._encode_transaction_data()

        data = hexstr_if_str(to_bytes, hexData)

        nonce = w3.eth.getTransactionCount(spender)
        gasPrice = w3.eth.gas_price

        tx = {
            'nonce': nonce,
            'to': tokenAddr,
            'data': data,
            'gas': estimateGas,
            'gasPrice': gasPrice,
        }
        signedTx = w3.eth.account.signTransaction(tx, spenderPrivateKey)

        txHash = w3.eth.sendRawTransaction(signedTx.rawTransaction)
        return w3.toHex(txHash)

    # Transfers the ownership of an NFT from one address to another address.
    # required arguments.
    # token address, owner address, spender address, spenderPrivateKey, receiver address, tokenId. 

    def safeTransferFrom(tokenAddr, ownerAddress, spenderAddress,  spenderPrivateKey, receiver, tokenId):

        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc721abi)

        owner = Web3.toChecksumAddress(ownerAddress)
        receiverAddres = Web3.toChecksumAddress(receiver)
        spender = Web3.toChecksumAddress(spenderAddress)

        transferData = contractInstance.functions.safeTransferFrom(
            owner, receiverAddres, tokenId)

        estimateGas = transferData.estimateGas({   
            'from': spender,
        })

        hexData = transferData._encode_transaction_data()

        data = hexstr_if_str(to_bytes, hexData)

        nonce = w3.eth.getTransactionCount(spender)
        gasPrice = w3.eth.gas_price

        tx = {
            'nonce': nonce,
            'to': tokenAddr,
            'data': data,
            'gas': estimateGas,
            'gasPrice': gasPrice,
        }
        signedTx = w3.eth.account.signTransaction(tx, spenderPrivateKey)

        txHash = w3.eth.sendRawTransaction(signedTx.rawTransaction)
        return w3.toHex(txHash)
