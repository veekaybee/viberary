package main

import (
	"fmt"
	"github.com/go-redis/redis"
	"html/template"
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

func search(query string) []string {
	// This is where you would implement the search logic to get the results
	// For this example, we'll just return some dummy data
	return []string{"Result 1", "Result 2", "Result 3"}
}

func main() {

	// Handle form requests

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// Serve the index.html file
		http.ServeFile(w, r, "./static/index.html")
	})

	http.HandleFunc("/search", func(w http.ResponseWriter, r *http.Request) {
		// Get the search query from the form input
		query := r.URL.Query().Get("query")

		// Pass the query to the search function to get the results
		results := search(query)

		// Add results to Redis
		client.Set(query, 1.0, 0)

		// Render the results template with the results on the homepage
		tmpl := template.Must(template.ParseFiles("./static/results.html"))
		tmpl.Execute(w, results)
	})

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
