package main


import (
    "fmt"
    "net"
    "bytes"
    "os"
    "log"
    "sflow_agent/sflow"
    "helper"

    //"reflect"
)

func simple_print(datagram *sflow.Datagram){
    fmt.Println("Datagram::Sflow version:",datagram.Version)
    fmt.Println("Datagram::IP version:",datagram.IpVersion)
    fmt.Println("Datagram::Ip address:",datagram.IpAddress)
    fmt.Println("Datagram::SubAgent Id:",datagram.SubAgentId)
    fmt.Println("Datagram::Sequence Num:",datagram.SequenceNumber)
    fmt.Println("Datagram::Uptime:",datagram.Uptime)
    fmt.Println("Datagram::NumSamples:",datagram.NumSamples)
    for i:=0; uint32(i) < datagram.NumSamples; i++ {
    // currently we only care about counter sample
        sample := datagram.Samples[i].(*sflow.CounterSample)

        fmt.Println("Sample::Seq:", sample.SequenceNum)
        fmt.Println("Sample::SourceId_type", sample.SourceIdType)
        fmt.Println("Sample::SourceId_Index_val", sample.SourceIdIndexVal)
        records := sample.GetRecords()
        for _, record := range records {
            //fmt.Println(reflect.ValueOf(record))
            counter_record := record.(sflow.GenericInterfaceCounters)
            fmt.Println("ifindex:",counter_record.Index)
            fmt.Println("InOctets:",counter_record.InOctets)
            fmt.Println("InUnicastPackets:",counter_record.InUnicastPackets)
            fmt.Println("InDiscards:",counter_record.InDiscards)
            fmt.Println("InErrors:",counter_record.InErrors)
            fmt.Println("OutOctets:",counter_record.OutOctets)
            fmt.Println("OutUnicastPackets:",counter_record.OutUnicastPackets)
            fmt.Println("OutDiscards:",counter_record.OutDiscards)
            fmt.Println("OutErrors:",counter_record.OutErrors)
        }
    }
}

func postData(datagram *sflow.Datagram, log *LogFile){
    for i:=0; uint32(i) < datagram.NumSamples; i++ {
    // currently we only care about counter sample
        sample := datagram.Samples[i].(*sflow.CounterSample)
        records := sample.GetRecords()
        for _, record := range records {
            //fmt.Println(reflect.ValueOf(record))
            counter_record := record.(sflow.GenericInterfaceCounters)
            data := map[string] string{
                "uuid": counter_record.Index,
                "host": os.Hostname(),
                "inDiscard": counter_record.InDiscards,
                "inError": counter_record.InErrors,
                "inBps": counter_record.InOctets,
                "inPps": counter_record.InUnicastPackets,
                "outDiscard": counter_record.OutDiscards,
                "outError": counter_record.OutErrors,
                "outBps": counter_record.OutOctets,
                "outPps": counter_record.OutUnicastPackets,   
            }
            err := YunhaiPost(data, log)
            if err != nil {
                msg := fmt.Sprintf("Error posting counter record: %v ", counter_record)
                log.logErr(msg, err)
            }

        }
    }
}

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
    log := helper.NewLogFile()
    log.BeginLogFile("sflow_agent")
    defer log.EndLogFile()
    defer socket.Close()

    // main loop
    for {
        data := make([]byte, 1024)
        //read, remoteAddr, err := socket.ReadFromUDP(data)
        _, _, err = socket.ReadFromUDP(data)
        if err != nil {
            log.LogErr("Error reading UDP packet", err)
            continue
        }
        data_reader := bytes.NewReader(data)
        decoder := sflow.NewDecoder(data_reader)
        datagram, err := decoder.Decode()
        if err !=nil {
            log.LogErr("Error decoding UDP packet", err)
            continue
        }
        postData(datagram, log)
    }
}