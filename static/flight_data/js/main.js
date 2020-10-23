//
//  Function Declarations
//
function getResult(url) {
    return new Promise((resolve, reject) => fetch(url)
        .then(response => {
            if (response.status !== 200) {
                throw `${response.status}: ${response.statusText}`;
            }
            response.json().then(data => {
                resolve(data)
            }).catch(reject)
        }).catch(reject)
    )
}

// TODO - set hostname dynamically
function getAllResults(progress, url, results = []) {
    return new Promise((resolve, reject) => fetch(url)
        .then(response => {
            if (response.status !== 200) {
                throw `${response.status}: ${response.statusText}`;
            }
            response.json().then(data => {
                results = results.concat(data.results);

                if (data.next) {
                    progress && progress(results);
                    getAllResults(progress, data.next, results).then(resolve).catch(reject)
                } else {
                    resolve(results);
                }
            }).catch(reject);
        }).catch(reject));
}

function progressCallback(results) {
    // render progress
    console.log(`${results.length} loaded`);
}

function journey_time_str(journey_ms) {
    let diff_hrs = Math.floor((journey_ms % 86400000) / 3600000); // hours
    let diff_mins = Math.round(((journey_ms % 86400000) % 3600000) / 60000); // minutes
    return diff_hrs + ' hrs ' + diff_mins + ' mins';
}

//
//  Main
//
// What’s the average journey time between London Heathrow (LHR) and Dubai (DXB)?
getAllResults(progressCallback, "/api/flights/?dep_air=LHR&dest_air=DXB&fields=out_arrival_date,out_arrival_time,out_depart_date,out_depart_time")
    .then(results => {
        let journeys_ms = results.map(p => new Date(p.out_arrival_date + ' ' + p.out_arrival_time)
            - new Date(p.out_depart_date + ' ' + p.out_depart_time)
        )

        let sum = 0;
        for (let i = 0; i < journeys_ms.length; i++) {
            sum += journeys_ms[i];
        }

        document.getElementById('avg-journey').innerHTML = journey_time_str(Math.floor(sum / journeys_ms.length));
    })
    .catch(console.error);

// Which airport day has the most departures from Manchester (MAN)?
getAllResults(progressCallback, "http://127.0.0.1:8000/api/flights/?dep_air=MAN&fields=out_depart_date")
    .then(results => {
        const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

        // Get the grouped counts
        const counts = results.reduce((p, c) => {
            const out_depart_date = new Date(c.out_depart_date).getDay();
            if (!p.hasOwnProperty(out_depart_date)) {
                p[out_depart_date] = 0;
            }
            p[out_depart_date]++;
            return p;
        }, {});

        const busiest_day = Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b);
        document.getElementById('man-day').innerHTML = days[busiest_day];
    })

// What proportion of the flights are business class?
getResult("http://127.0.0.1:8000/api/flights/count/")
    .then(total_result => {
        getResult("http://127.0.0.1:8000/api/flights/count/?out_flight_class=Business")
            .then(business_result => {
                const business_ratio = Math.round((business_result.count / total_result.count) * 100)
                document.getElementById('business-ratio').innerHTML = business_ratio + '%';
            })
    })

// What percentage of the total set of flights fly into Sweden?
getAllResults(progressCallback, "http://127.0.0.1:8000/api/airports/?iso_country=SE&fields=iata_code")
    .then(results => {
        const se_codes = results.map(p => p.iata_code)
        const base_url = "http://127.0.0.1:8000/api/flights/?dest_air="
        const req_url = base_url + se_codes.join(',')

        getResult("http://127.0.0.1:8000/api/flights/count/")
            .then(total_result => {
                getResult(req_url)
                    .then(se_result => {
                        const se_ratio = (se_result.count / total_result.count).toFixed(4) * 100
                        document.getElementById('sweden-flights').innerHTML = se_ratio + '%';
                    })
            })
    })

// What is the average cost of a transatlantic flight?
// TODO - This could be way improved, perhaps with a post, or nesting airports in flights
getAllResults(progressCallback, "http://127.0.0.1:8000/api/airports/?continent=NA&fields=iata_code")
    .then(results => {
        const na_codes = results.map(p => p.iata_code)
        const base_url = "http://127.0.0.1:8000/api/flights/?dest_air="
        const req_url = base_url + na_codes.join(',')

        fx.base = "GBP";
        fx.rates = {
            "AUD": 1.84, // eg. 1 USD === 0.745101 EUR
            "ZAR": 21.21, // etc...
            "ARS": 101.90,
            "GBP": 1,        // always include the base rate (1:1)
            /* etc */
        }

        function convert(val, from) {
            result = val;
            if (from !== "GBP") {
                fx.convert(val, {from: from, to: "GBP"});
            }
            return val;
        }

        getAllResults(progressCallback, req_url)
            .then(na_results => {
                let prices = na_results.map(p => convert(p.original_price, p.original_currency))

                let sum = 0;
                for (let i = 0; i < prices.length; i++) {
                    sum += parseFloat(prices[i]);
                }

                console.log(Math.floor(sum / prices.length))
                document.getElementById('trans-atlantic-cost').innerHTML = '£' + Math.floor(sum / prices.length);
            })
    })