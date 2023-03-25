package main

import (
	"fmt"
	"github.com/go-redis/redis"
	"log"
	"net/http"
)

var client *redis.Client

func formHandler(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		fmt.Fprintf(w, "ParseForm() err: %v", err)
		return
	}
	fmt.Fprintf(w, "POST request successful ")
	query := r.FormValue("query")

	fmt.Fprintf(w, "query = %s\n", query)

	client.Set(query, 1.0, 0)
}

func main() {

	// Handle form requests
	fileServer := http.FileServer(http.Dir("./static"))

	http.Handle("/", fileServer)
	http.HandleFunc("/form", formHandler)

	fmt.Printf("Starting server at port 8080\n")

	// Connect to local Redis
	client = redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "",
		DB:       0,
	})

	fmt.Printf("Connecting to Redis\n")

	pong, err := client.Ping().Result()
	fmt.Println(pong, err)

	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}
