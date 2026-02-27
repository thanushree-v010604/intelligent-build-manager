```c
// Facebook C API Example

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>

size_t write_memory_callback(void *ptr, size_t size, size_t nmemb, void *data) {
    return size * nmemb;
}

int main() {
    CURL *curl;
    CURLcode res;
    std::string url = "https://www.facebook.com/";

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_memory_callback);
        res = curl_easy_perform(curl);
        if(res != CURLE_OK) {
            printf("cURL error: %s\n", curl_easy_strerror(res));
        }
        curl_easy_cleanup(curl);
    }
    curl_global_cleanup();
    return 0;
}
```

Please note that Facebook's Terms of Service prohibit scraping their website, so use this code for educational purposes only.