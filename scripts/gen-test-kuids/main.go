package main

import (
	"encoding/hex"
	"encoding/json"
	"log"
	"math"
	"os"
	"strings"
	"time"

	"github.com/segmentio/ksuid"
)

var minTime int64 = 1400000000               // ksuid epoch
var maxTime int64 = math.MaxUint32 + minTime // ksuid upper bound

type ksuidInfo struct {
	Timestamp int64  `json:"timestamp"`
	Payload   string `json:"payload"`
	KSUID     string `json:"ksuid"`
}

// linSpace returns evenly spaced numbers over a specified interval.
// like numpy.linspace
func linSpace(start, stop, num int64) (res []int64) {
	if num <= 0 {
		return []int64{}
	}
	if num == 1 {
		return []int64{start}
	}
	interval := (stop - start) / (num - 1)

	res = make([]int64, num)
	res[0] = start

	var i int64
	for i = 1; i < num; i++ {
		res[i] = start + i*interval
	}
	res[num-1] = stop
	return
}

func main() {
	testFile, err := os.OpenFile("../../tests/test_kuids.txt", os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0755)
	if err != nil {
		log.Fatal(err)
	}
	defer testFile.Close()

	stamps := linSpace(minTime, maxTime, 1000)
	for _, stamp := range stamps {
		t := time.Unix(stamp, 0).UTC()
		uid, err := ksuid.NewRandomWithTime(t)
		if err != nil {
			log.Fatal(err)
		}

		json, err := json.Marshal(ksuidInfo{
			Timestamp: stamp,
			Payload:   strings.ToUpper(hex.EncodeToString(uid.Payload())),
			KSUID:     uid.String(),
		})
		if err != nil {
			log.Fatal(err)
		}
		_, err = testFile.Write(json)
		if err != nil {
			log.Fatal(err)
		}
		_, err = testFile.WriteString("\n")
		if err != nil {
			log.Fatal(err)
		}
	}
	testFile.Sync()
}
