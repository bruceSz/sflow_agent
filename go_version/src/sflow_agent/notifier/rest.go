package notifier

import (
    "net/http"
    "fmt"
    "bytes"
    "encoding/json"
    "sflow_agent/helper"
)

func test_req_data() (map[string]string){
    data := map[string]string{
       "uuid": "test-zs-1",
       "host": "test.baidu.com",
       "inDiscard": "-1",
       "inError":"-1",
       "inBps":"-1",
       "inPps": "-1",
       "outDiscard": "-1",
       "outError":"-1",
       "outBps":"-1",
       "outPps":"-1",
    }
    return data
}

func YunhaiPost(data map[string]string, log *helper.LogFile) (err error){
    client := &http.Client{}
    json_data, err := json.Marshal(data)
    if err != nil {
        fmt.Println("json err:",err)
        return err
    }
    body := bytes.NewBuffer([]byte(json_data))
    req, err := http.NewRequest("POST",
                                "http://net-api.yunhai.baidu.com:8855/api/v1/flows/summary/",
                                body)
    req.SetBasicAuth("neutron-api-user","neutron-api-secret")

    resp, err := client.Do(req)
    if err != nil {
        msg := fmt.Sprintf("error when posting data: %v ",data)
        log.LogErr(msg, err)
        fmt.Printf("Error: %s", err)
        return err
    }
    msg := fmt.Sprintf("Post data: %v ",data)
    log.LogMsg(msg)
    log.LogMsg(resp.Status)
    //fmt.Println(resp)
    return nil
}