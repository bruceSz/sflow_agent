package main

import "fmt"
import "errors" 

func main() {
    fmt.Println("hello")
    var flag errors = nil
    if ! flag {
        fmt.Println("good")
    }
}

