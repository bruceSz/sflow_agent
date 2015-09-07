package main


import (
    "fmt"
    "net"
    "bytes"
    "os"
    "sflow_agent/sflow"
    "reflect"
)

func main() {
    // create list socket
    socket, err := net.ListenUDP("udp4", &net.UDPAddr{
        IP:   net.IPv4(0, 0, 0, 0),
        Port: 6343,
    })
    if err != nil {
        fmt.Println("ListenUDP failed!", err)
        return
    }
    defer socket.Close()

    //for {
        // read socket
        data := make([]byte, 1024)
        //read, remoteAddr, err := socket.ReadFromUDP(data)
        _, _, err = socket.ReadFromUDP(data)
        if err != nil {
            fmt.Println("Read sflow packet from socket failed!", err)
            //continue
        }
    data_reader := bytes.NewReader(data)
    decoder := sflow.NewDecoder(data_reader)
    datagram, err := decoder.Decode()
    if err !=nil {
        fmt.Println("Decode error, ", err)
        os.Exit(1)
    }

    val_ptr := reflect.ValueOf(datagram)
    value := val_ptr.Elem()

    for i:=0; i < value.NumField()-1; i++ {
        if i != 2 {
            fmt.Println(value.Field(i).Uint())
        }
    }
        //fmt.Printf("%s\n\n", datagram)

    //}
}