
var output;
fetch("https://api.henrikdev.xyz/valorant/"+"v1/status/eu", {
    headers: {
        'Accept': 'application/json',
        'Authorization' : "HDEV-97a80cc7-cabb-4668-8df3-a4d07fae9f67"
    }
    })
    .then(response => response.text())
    .then(text => output = text)

console.log(output)
