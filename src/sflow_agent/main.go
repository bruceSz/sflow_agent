package main


import (
    "fmt"
    "net"
    "bytes"
    "os"
    "strconv"
    "sflow_agent/sflow"
    "sflow_agent/helper"
    "sflow_agent/notifier"

    //"reflect"
)

var HOSTNAME, _ =  os.Hostname()

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

func postData(datagram *sflow.Datagram, log *helper.LogFile){
    for i:=0; uint32(i) < datagram.NumSamples; i++ {
    // currently we only care about counter sample
        sample := datagram.Samples[i].(*sflow.CounterSample)
        records := sample.GetRecords()
        for _, record := range records {
            //fmt.Println(reflect.ValueOf(record))
            counter_record := record.(sflow.GenericInterfaceCounters)
            data := map[string] string{
                "uuid": strconv.FormatUint(uint64(counter_record.Index),10),
                "host": HOSTNAME,
                "inDiscard": strconv.FormatUint(uint64(counter_record.InDiscards), 10),
                "inError": strconv.FormatUint(uint64(counter_record.InErrors), 10),
                "inBps": strconv.FormatUint(counter_record.InOctets, 10),
                "inPps": strconv.FormatUint(uint64(counter_record.InUnicastPackets), 10),
                "outDiscard": strconv.FormatUint(uint64(counter_record.OutDiscards), 10),
                "outError": strconv.FormatUint(uint64(counter_record.OutErrors), 10),
                "outBps": strconv.FormatUint(counter_record.OutOctets, 10),
                "outPps": strconv.FormatUint(uint64(counter_record.OutUnicastPackets), 10),
            }
            err := notifier.YunhaiPost(data, log)
            if err != nil {
                msg := fmt.Sprintf("Error posting counter record: %v ", counter_record)
                log.LogErr(msg, err)
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