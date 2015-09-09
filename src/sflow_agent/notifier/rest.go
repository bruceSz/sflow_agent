package notifier

import (
    "net/http"
    "fmt"
    "bytes"
    "encoding/json"
)

func test_req_data() (map[string]string){
    data := map[string]string{
       "uuid": "test-zs",
       "hostname": "test.baidu.com",
       "in_discard": "-1",
       "in_error":"-1",
       "in_bps":"-1",
       "in_pps": "-1",
       "out_discard": "-1",
       "out_error":"-1",
       "out_bps":"-1",
       "out_pps":"-1",
    }
    return data
}

func YunhaiPost(data map[string]string) (ret_code int,ret_msg string) {
    client := &http.Client{}
    json_data, err := json.Marshal(data)
    if err != nil {
        fmt.Println("json err:",err)
    }
    body := bytes.NewBuffer([]byte(json_data))
    req, err := http.NewRequest("POST",
                                "http://net-api.yunhai.baidu.com:8855/api/v1/flows/summary/",
                                body)
    req.SetBasicAuth("neutron-api-user","neutron-api-secret")

    resp, err := client.Do(req)
    if err != nil {
        fmt.Printf("Error: %s", err)
    }
    fmt.Println(resp)

}