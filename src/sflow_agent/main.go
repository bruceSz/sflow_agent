package main


import (
    "fmt"
    "net"
    //"sflow_agent/sflow"
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

    for {
        // read socket
        data := make([]byte, 1024)
        read, remoteAddr, err := socket.ReadFromUDP(data)
        if err != nil {
            fmt.Println("Read sflow packet from socket failed!", err)
            continue
        }
        fmt.Printf("%x\n\n", data)

    }
}
