package main

import (
    "net/http" 
    "fmt"
)

func main() {
    client := &http.Client{}
    req, err := http.NewRequest("GET", 
                                "http://net-api.yunhai.baidu.com:8855/api/v1/flows/summary/", 
                                nil)
    req.SetBasicAuth("neutron-api-user","neutron-api-secret")
    resp, err := client.Do(req)
    if err != nil {
        fmt.Printf("Error: %s", err)
    }
    fmt.Println(resp)

}
