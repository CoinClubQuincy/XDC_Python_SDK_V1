from web3 import web3_Request
from net import net_Request
from eth import eth_Request
from tatum import tatum_Request

import hashlib 

class Test:
    def __init__(self):
        print("---------------- Starting Web3 Test ----------------")
        #self.web3_test()

        print("---------------- Starting net Test ----------------")
        #self.net_test()

        print("---------------- Starting eth Test ----------------")
        #self.eth_test()

        print("---------------- Starting tatum Test ----------------")
        self.tatum_test()


    def web3_test(self):
        String= "Q"
        Hash =  hashlib.sha256(String.encode('utf-8')).hexdigest()
        #print(Hash)

        #print(web3_Request.clientVersion())
        #print(web3_Request.sha3(Hash=Hash))

    def net_test(self):
        print("none")
        #print(net_Request.version())
        #print(net_Request.listening())
        #print(net_Request.peerCount())
        
    def eth_test(self):
        #print(int(eth_Request.protocolVersion(form="Text"),16))
        #print(eth_Request.syncing(form="Text"))
        #print(eth_Request.coinbase(form="Text"))
        print(eth_Request.gasPrice(form="Text"))
        print(eth_Request.accounts(form="Text"))
        print(eth_Request.blockNumber(form="Text"))
       

        Addy = "0x438e0b511981FE8CF7283e981ca8c3394bB3646E"
        #print(eth_Request.getBalance(Address=Addy,form="Text"))

        #print(eth_Request.getTransactionCount(form="Text"))
        #print(eth_Request.getBlockTransactionCountByHash(form="Text"))
        #print(eth_Request.getBlockTransactionCountByNumber(form="Text"))
        #print(eth_Request.getCode(form="Text"))
        #print(eth_Request.call(form="Text"))
        #print(eth_Request.estimateGas(form="Text"))
        #print(eth_Request.getBlockByHash(form="Text"))
        #print(eth_Request.getBlockByNumber(form="Text"))
        #print(eth_Request.getBlockSignersByNumber(form="Text"))
        #print(eth_Request.getBlockSignersByHash(form="Text"))
        #print(eth_Request.getBlockFinalityByNumber(form="Text"))
        #print(eth_Request.getBlockFinalityByHash(form="Text"))
        #print(eth_Request.getCandidateStatus(form="Text"))
        #print(eth_Request.getTransactionByHash(form="Text"))
        #print(eth_Request.getTransactionByBlockHashAndIndex(form="Text"))
        #print(eth_Request.getTransactionByBlockNumberAndIndex(form="Text"))
        #print(eth_Request.getTransactionReceipt(form="Text"))
        
        #ERRORS
        #print(eth_Request.getCandidates())
        #print(eth_Request.sendRawTransaction())
        #print(eth_Request.getStorageAt())
        #print(eth_Request.sign())
        #print(eth_Request.sendTransaction())

    def tatum_test(self):
        API_KEY = "b56527b4-1db2-4842-b388-357a7ad44d2a"
        Seed = "Quincy_JOJONONONO"
        Hash = "0xead075790098c7261e9fad995183fcc6eb4c3102f22c2507fc0fc25bd2cd0aa9"
        Address = "xdce4c4febe1cb34c3490167c163c9ed92049b32b5c" 
        xpub = tatum_Request.Generate_XDC_Wallet(Seed,API_KEY,form="Text")
        
        print(xpub)
        print(tatum_Request.Generate_XDC_Wallet_EPK(API_KEY,xpub,index=0))
        print(tatum_Request.Generate_XDC_Private_key(API_KEY,Seed,form="Text"))
        print(tatum_Request.Web3_HTTP_Driver(API_KEY,form="Text"))
        print(tatum_Request.Current_Block_Number(API_KEY,form="Text"))
        print(tatum_Request.XDC_Block_by_Hash(API_KEY,Hash,form="Text"))
        print(tatum_Request.XDC_Account_Balance(API_KEY,Address,form="Text"))
        blockHash,blockNumber,From,gas,gasPrice,input,nonce,To,transactionIndex,value,contractAddress,cumulativeGasUsed,gasUsed,logs = tatum_Request.XDC_Transaction(API_KEY,Hash,form="Text")

        print(tatum_Request.Count_Outgoing_XDC_Transactions(API_KEY,Address,form="Text"))

        #print(tatum_Request.Send_XDC_ERC20(API_KEY,form="Text"))
        #print(tatum_Request.Estimate_XDC_Transaction_Fees(API_KEY,form="Text"))

        print(blockNumber)
if __name__ == "__main__":
    Test()
