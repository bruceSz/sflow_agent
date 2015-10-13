package helper
// TODO: thread safe
import (
    "fmt"
    "log"
    "os"
    "time"
)

// log struct
type LogFile struct {
    mFile       *os.File
    mLogger     *log.Logger
}


func NewLogFile() *LogFile {
    return &LogFile{mFile:nil, mLogger:nil}
}

func (logFile *LogFile) BeginLogFile(fileName string) error {
    strTime := time.Now().Format("20060102_150405")
    logFileName := GetCurPath() + "/" + fileName + "_" + strTime + ".log"
    mFile, err := os.OpenFile(logFileName, os.O_RDWR|os.O_CREATE, 0777)
    if err != nil {
        return err
    }

    logFile.mLogger = log.New(mFile, "\r\n", 
        log.Ldate|log.Ltime|log.Llongfile)
    logFile.mFile = mFile
    return nil
}

func (logFile *LogFile) EndLogFile() {
    if logFile.mFile != nil {
        fmt.Println("close the file")
        logFile.mFile.Close()
    }
}
// Fatal msg
func (logFile *LogFile) LogFatal(msg string, err error) {  
    if err != nil {  
        logFile.mLogger.Fatalf("Fatal: "+msg+"  %v\n", err)
    }  
}

// Error msg  
func (logFile *LogFile) LogErr(msg string, err error) {  
    if err != nil {  
        logFile.mLogger.Printf("Err: "+msg+" %v\n", err) //记录到文件里  
    }  
} 
// normal msg  
func (logFile *LogFile) LogMsg(msg string) {  
    logFile.mLogger.Printf("Msg: %v\n", msg) //记录到文件里  
}

func GetCurPath() (path string) {
    pwd, err := os.Getwd()
    if err != nil {
        fmt.Errorf("Get wd error: ",err)
        os.Exit(1)
    }
    return pwd
}

func main() {
    log  := NewLogFile()
    err := log.BeginLogFile("test_log")
    if err != nil {
        fmt.Errorf("create log failed")
    }
    log.LogMsg("hhaa")
    log.EndLogFile()
}
