package sflow

import (
    "encoding/binary"
    "io"
    "unsafe"
)

// GenericInterfaceCounters is a generic switch counters record.
type GenericInterfaceCounters struct {
    Index               uint32
    Type                uint32
    Speed               uint64
    Direction           uint32
    Status              uint32
    InOctets            uint64
    InUnicastPackets    uint32
    InMulticastPackets  uint32
    InBroadcastPackets  uint32
    InDiscards          uint32
    InErrors            uint32
    InUnknownProtocols  uint32
    OutOctets           uint64
    OutUnicastPackets   uint32
    OutMulticastPackets uint32
    OutBroadcastPackets uint32
    OutDiscards         uint32
    OutErrors           uint32
    PromiscuousMode     uint32
}


var (
    genericInterfaceCountersSize = uint32(unsafe.Sizeof(GenericInterfaceCounters{}))

)

// RecordType returns the type of counter record.
func (c GenericInterfaceCounters) RecordType() int {
    return TypeGenericInterfaceCountersRecord
}

func decodeGenericInterfaceCountersRecord(r io.Reader, length uint32) (GenericInterfaceCounters, error) {
    c := GenericInterfaceCounters{}
    b := make([]byte, int(length))
    n, _ := r.Read(b)
    if n != int(length) {
        return c, ErrDecodingRecord
    }

    fields := []interface{}{
        &c.Index,
        &c.Type,
        &c.Speed,
        &c.Direction,
        &c.Status,
        &c.InOctets,
        &c.InUnicastPackets,
        &c.InMulticastPackets,
        &c.InBroadcastPackets,
        &c.InDiscards,
        &c.InErrors,
        &c.InUnknownProtocols,
        &c.OutOctets,
        &c.OutUnicastPackets,
        &c.OutMulticastPackets,
        &c.OutBroadcastPackets,
        &c.OutDiscards,
        &c.OutErrors,
        &c.PromiscuousMode,
    }

    return c, readFields(b, fields)
}

func (c GenericInterfaceCounters) encode(w io.Writer) error {
    var err error

    err = binary.Write(w, binary.BigEndian, uint32(c.RecordType()))
    if err != nil {
        return err
    }

    err = binary.Write(w, binary.BigEndian, genericInterfaceCountersSize)
    if err != nil {
        return err
    }

    err = binary.Write(w, binary.BigEndian, c)
    return err
}

