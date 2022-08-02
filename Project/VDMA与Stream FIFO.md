FIFO上的AXI4是FULL 5通道3W2R全双工
通道: 有自己的valid和ready

## Programming Sequence Using Example Software Driver
![[Pasted image 20220802141407.png]]
### Init Sequence  
Call the function *XLlFifo_CfgInitialize* for the initialization that does a reset of the  
TX/RX registers and then clear the ISR.  
### Transmit a Packet  
1. Call *SetupInterruptSystem* function which does the initialization of the interrupt  
controller  
2. Call the function *XLlFifo_IntEnable* to enable all the required interrupts.  
3. Call the *TxSend* function to write the data to TXFIFO and check TDFV for the FIFO  
occupancy before writing to the TX FIFO using the *XLFifo_iTxVacancy* function.  
4. Start transmission by writing to TLR using the *XLIFifo_iTxSetLen* function.  
5. Wait for the data transmission to complete, then the call *FifoHandler* interrupt  
handler and if it is a TX complete, then call FifoSendHandler and then clear the ISR.  
### Receive a Packet:  
1. On receiving the RX Interrupt, the *FifoHandler* interrupt handler is called which in  
turn calls the *FifoRecvHandler*.
2. Read RLR to find the number of bytes.  
3. Read the number of bytes till the number of bytes read from RLR while checking the  
occupancy by using the *XLlFifo_iRxOccupancy* function.  
4. Clear the ISR.  
5. Check if there is an Interrupt pending for Rx and then go to step2.
