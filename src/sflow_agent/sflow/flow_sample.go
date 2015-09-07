package sflow

import (
    //"bytes"
    //"encoding/binary"
    //"errors"
    "io"
)

const (
    TypeRawPacketFlowRecord     = 1
    TypeEthernetFrameFlowRecord = 2
    TypeIpv4FlowRecord          = 3
    TypeIpv6FlowRecord          = 4

    TypeExtendedSwitchFlowRecord     = 1001
    TypeExtendedRouterFlowRecord     = 1002
    TypeExtendedGatewayFlowRecord    = 1003
    TypeExtendedUserFlowRecord       = 1004
    TypeExtendedUrlFlowRecord        = 1005
    TypeExtendedMlpsFlowRecord       = 1006
    TypeExtendedNatFlowRecord        = 1007
    TypeExtendedMlpsTunnelFlowRecord = 1008
    TypeExtendedMlpsVcFlowRecord     = 1009
    TypeExtendedMlpsFecFlowRecord    = 1010
    TypeExtendedMlpsLvpFecFlowRecord = 1011
    TypeExtendedVlanFlowRecord       = 1012
)

type FlowSample struct {
    SequenceNum      uint32
    SourceIdType     byte
    SourceIdIndexVal uint32 // NOTE: this is 3 bytes in the datagram
    SamplingRate     uint32
    SamplePool       uint32
    Drops            uint32
    Input            uint32
    Output           uint32
    numRecords       uint32
    Records          []Record
}

// SampleType returns the type of sFlow sample.
func (s *FlowSample) SampleType() int {
    return TypeFlowSample
}

func (s *FlowSample) GetRecords() []Record {
    return s.Records
}

func decodeFlowSample(r io.ReadSeeker) (Sample, error) {
    // TODO
    return nil, nil
}

func (s *FlowSample) encode(w io.Writer) error {
    // TODO
    return nil
}
