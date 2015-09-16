package main

import (
    "fmt"
    "os/exec"
    "strings"
    "io/ioutil"
)
func get_qvo_ports() ([]string){
    var ret  []string
    cmd := exec.Command("ovs-vsctl","list-ports","br-int")
    output, _:= cmd.Output()
    ports := string(output)
    port_list := strings.Split(ports, "\n")
    for _, port := range port_list {
        if port != "patch-tun" {
            ret = append(ret, port)
        }
    }
    return ret

}
func get_uuids() ([] string) {
    ps -ef|grep qemu-kvm|grep -e  "-uuid [[:alnum:]]\{8\}-[[:alnum:]]\{4\}-[[:alnum:]]\{4\}-[[:alnum:]]\{4\}-[[:alnum:]]\{12\}" -o
    ps -ef|grep instance-6c80b29b-071c-4eb6-83c2-ce3ad60224a6|grep -v grep |egrep -e "-uuid [[:alnum:]]+-[[:alnum:]]+-[[:alnum:]]+-[[:alnum:]]+-[[:alnum:]]+" --color  -o
}

func get_tap_devices() ([] string) {
    var ret [] string
    //cmd := exec.Command("virsh list|awk '/running/{print $1}'|xargs -I{} virsh domiflist {}|grep tap|awk '{print $1}'")
    cmd1 := exec.Command("virsh", "list")
    cmd2 := exec.Command("awk", "/running/{print $1}")
    cmd3 := exec.Command("xargs", "-I{}", "virsh","domiflist","{}")
    cmd4 := exec.Command("awk", "/tap/{print $1}")
    cmd2.Stdin, _ = cmd1.StdoutPipe()
    cmd3.Stdin, _ = cmd2.StdoutPipe()
    cmd4.Stdin, _ = cmd3.StdoutPipe()
    output, _ := cmd4.StdoutPipe()


    cmd4.Start()
    cmd3.Start()
    cmd2.Start()
    cmd1.Run()
    ret_bytes, _ := ioutil.ReadAll(output)
    cmd4.Wait()
    taps := string(ret_bytes)
    tap_list := strings.Split(taps, "\n")
    for _, tap := range tap_list {
        ret = append(ret, tap)
    }
    fmt.Println(ret)
}

func main(){
    //#ret := get_qvo_ports()
    //#fmt.Println(ret)
    //#ret = get_tap_devices()
    //#fmt.Println(ret)
}