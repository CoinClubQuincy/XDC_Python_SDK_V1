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
with open('./common/xrc20abi.json') as abiJson:
    xrc20abi = json.load(abiJson)

# This is a class which consists all the methods as per XRC20 standards.

class XRC20:

    # Gets the Name of the specified address.
    # Token address is required as argument.

    def name(tokenAddr):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc20abi)
        name = contractInstance.functions.name().call()
        return name

    # Gets method returns total supply of token.
    # Token address is required as argument.

    def totalSupply(tokenAddr):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc20abi)
        totalSupply = contractInstance.functions.totalSupply().call()
        totalSupply = w3.fromWei(totalSupply, 'ether')
        return totalSupply

    # Gets the Decimal of the specified address.
    # Token address is required as argument.

    def decimal(tokenAddr):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc20abi)
        decimal = contractInstance.functions.decimals().call()
        return decimal

    # Gets the Symbol of the specified address.
    # Token address is required as argument.

    def symbol(tokenAddr):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc20abi)
        symbol = contractInstance.functions.symbol().call()
        return symbol

    # Gets the balance of the specified address.
    # token address, owner address are required as arguments.

    def balanceOf(tokenAddr, ownerAddress):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc20abi)
        owner = Web3.toChecksumAddress(ownerAddress)
        balance = contractInstance.functions.balanceOf(owner).call()
        return w3.fromWei(balance, 'ether')

    # This method returns how much allowance spender have from owner.
    # This function required three arguments.
    # owner address, spender address, token address.

    def allowance(tokenAddr, ownerAddress, spenderAddress):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc20abi)
        owner = Web3.toChecksumAddress(ownerAddress)
        spender = Web3.toChecksumAddress(spenderAddress)
        Allowance = contractInstance.functions.allowance(owner, spender).call()
        return w3.fromWei(Allowance, 'ether')

    # Transfer XDC for a specified address.
    # This function requires following arguments.
    # private key, recipient address, amount.

    def transferXDC(ownerAddress, receiverAddress, ownerPrivateKey, amount):

        owner = Web3.toChecksumAddress(ownerAddress)
        spender = Web3.toChecksumAddress(receiverAddress)
        amount = w3.toWei(amount, 'ether')

        nonce = w3.eth.getTransactionCount(owner)
        gasPrice = w3.eth.gas_price
        estimateGas = w3.eth.estimateGas({
            'to': spender,
            'from': owner,
            'value': amount
        })

        tx = {
            'nonce': nonce,
            'to': spender,
            'value': amount,
            'gas': estimateGas,
            'gasPrice': gasPrice,
        }

        signedTx = w3.eth.account.signTransaction(tx, ownerPrivateKey)

        txHash = w3.eth.sendRawTransaction(signedTx.rawTransaction)
        return w3.toHex(txHash)

    # Transfer token for a specified address.
    # This function requires following arguments.
    # ownerAddress, ownerPrivateKey, receiver address, token address, amount.

    def transferToken(tokenAddr, ownerAddress, ownerPrivateKey,  receiverAddress, amount):

        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc20abi)

        owner = Web3.toChecksumAddress(ownerAddress)
        spender = Web3.toChecksumAddress(receiverAddress)

        balance = contractInstance.functions.balanceOf(owner).call()

        if amount > balance:
            return "amount exceeds balance"

        amount = w3.toWei(amount, 'ether')

        Transfer = contractInstance.functions.transfer(spender, amount)

        hexData = Transfer._encode_transaction_data()

        data = hexstr_if_str(to_bytes, hexData)

        estimateGas = Transfer.estimateGas(
            {
                'from': owner,
            }
        )

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

    # Approve the passed address to spend the specified amount of tokens on behalf of owner.
    # This function required arguments.
    # ownerAddress, ownerPrivateKey, spenderAddress, tokenAddr, amount.

    def approve(tokenAddr, ownerAddress, ownerPrivateKey,  spenderAddress, amount):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc20abi)

        owner = Web3.toChecksumAddress(ownerAddress)
        spender = Web3.toChecksumAddress(spenderAddress)

        balance = contractInstance.functions.balanceOf(owner).call()
        allowanceAmount = contractInstance.functions.allowance(
            owner, spender).call()

        if amount > balance and allowanceAmount > balance:
            return "amount exceeds balance"

        amount = w3.toWei(amount, 'ether')

        approveData = contractInstance.functions.approve(spender, amount)

        hexData = approveData._encode_transaction_data()

        data = hexstr_if_str(to_bytes, hexData)

        estimateGas = approveData.estimateGas()

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

    # increase the amount of tokens that an owner allowed to a spender.
    # This function required arguments.
    # owner address, ownerPrivateKey, spender address, token address, amount.

    def increaseAllowance(tokenAddr, ownerAddress, ownerPrivateKey,  spenderAddress, amount):

        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc20abi)

        owner = Web3.toChecksumAddress(ownerAddress)
        spender = Web3.toChecksumAddress(spenderAddress)

        balance = contractInstance.functions.balanceOf(owner).call()

        allowanceAmount = contractInstance.functions.allowance(
            owner, spender).call()

        allowanceAmount = w3.fromWei(allowanceAmount, 'ether')

        totalAmount = allowanceAmount + amount

        if totalAmount > balance:
            return "amount exceeds balance"

        totalAmount = w3.toWei(totalAmount, 'ether')

        Transfer = contractInstance.functions.approve(spender, totalAmount)

        hexData = Transfer._encode_transaction_data()

        data = hexstr_if_str(to_bytes, hexData)

        estimateGas = Transfer.estimateGas()

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

    # decrease the amount of tokens that an owner allowed to a spender.
    # This function required arguments.
    # owner address, ownerPrivateKey, spender address, token address, amount.

    def decreaseAllowance(tokenAddr, ownerAddress, ownerPrivateKey,  spenderAddress, amount):
        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc20abi)

        owner = Web3.toChecksumAddress(ownerAddress)
        spender = Web3.toChecksumAddress(spenderAddress)

        allowanceAmount = contractInstance.functions.allowance(
            owner, spender).call()
        allowanceAmount = (w3.fromWei(allowanceAmount, 'ether'))

        if allowanceAmount >= amount:
            totalAmount = allowanceAmount - amount
        else:
            totalAmount = amount - allowanceAmount

        totalAmount = w3.toWei(totalAmount, 'ether')

        approveData = contractInstance.functions.approve(spender, totalAmount)

        hexData = approveData._encode_transaction_data()

        data = hexstr_if_str(to_bytes, hexData)

        estimateGas = approveData.estimateGas()

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

    # Transfer tokens from one address to another.
    # This function requires following arguments.
    # owner address, spenderPrivateKey, spender address, receiver address, token address, amount.

    def transferFrom(tokenAddr, ownerAddress,  spenderPrivateKey,  spenderAddress, receiver, amount):

        contractInstance = w3.eth.contract(address=tokenAddr, abi=xrc20abi)

        owner = Web3.toChecksumAddress(ownerAddress)
        receiverAddres = Web3.toChecksumAddress(receiver)
        spender = Web3.toChecksumAddress(spenderAddress)

        amount = w3.toWei(amount, 'ether')

        transferData = contractInstance.functions.transferFrom(
            owner, receiverAddres, amount)

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
