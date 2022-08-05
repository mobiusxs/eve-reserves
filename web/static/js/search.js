function get_query() {
    const query = document.getElementById('query').value;
    const array = [query]
    return JSON.stringify(array);
}


function send_request(query) {
    const request = new XMLHttpRequest();
    request.open('POST', 'https://esi.evetech.net/latest/universe/ids/?datasource=tranquility&language=en', true);
    request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    request.onreadystatechange = function() {
        if (request.readyState === 4 && request.status === 200) {
            display_results(request.responseText);
        }
    }
    request.send(query);
}


function display_results(result_string) {
    reset_table();
    if (result_string === '{}') {
        display_empty_results();
    } else {
        display_populated_results(result_string);
    }
}


function reset_table() {
    const table = document.getElementById('results');
    table.textContent = '';
}


function display_empty_results() {
    const table = document.getElementById('results');
    const head = document.createElement('thead');
    const tr = document.createElement('tr');
    const td = document.createElement('td');
    td.innerText = 'No results found';
    tr.appendChild(td);
    head.appendChild(tr);
    table.appendChild(head);
}


function display_populated_results(result_string) {
    const table = document.getElementById('results');
    const head = document.createElement('thead');
    const body = document.createElement('tbody');
    let tr = document.createElement('tr')

    let td = document.createElement('td');
    td.innerText = 'Type';
    tr.appendChild(td)

    td = document.createElement('td');
    td.innerText = 'Name';
    tr.appendChild(td)

    td = document.createElement('td');
    td.innerText = 'ID';
    tr.appendChild(td);

    head.appendChild(tr);
    table.appendChild(head);

    const results = JSON.parse(result_string);
    for (let type in results) {
        for (const entity of results[type]) {

            type = type.slice(0, -1);  // remove trailing s
            type = capitalize(type);

            tr = document.createElement('tr');
            td= document.createElement('td');
            td.innerText = type;
            tr.appendChild(td);

            td= document.createElement('td');
            td.innerText = entity.name;
            tr.appendChild(td);

            td= document.createElement('td');
            td.innerText = entity.id;
            tr.appendChild(td);

            body.appendChild(tr);
        }
    }
    table.appendChild(body);
}


function capitalize(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}


function search() {
    const query = get_query();
    send_request(query);
}
