function calculateResult() {
    var input = document.getElementById("input").value;

    // Send the input value to the server-side Python code using AJAX
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/submit");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // Update the webpage with the result received from the server
            var result = JSON.parse(xhr.responseText).result;
            var resultDiv = document.getElementById("result");
            resultDiv.innerText = "Result: " + result;

            // Call the updateHistory function with the result
            updateHistory(result);
        }
    };
    xhr.send("input_name=" + input);
}

function updateHistory(result) {
    const output = document.getElementById("output");
    const outputSection = document.getElementById("output-section");

    const entry = document.createElement("div");
    entry.className = "entry";

    const deleteButton = document.createElement("button");
    deleteButton.className = "delete-button";
    deleteButton.innerHTML = "−";
    deleteButton.onclick = function () {
        entry.remove();
    };
    entry.appendChild(deleteButton);

    const entryText = document.createElement("span");
    entryText.innerHTML = result;
    entry.appendChild(entryText);

    output.appendChild(entry);

    // Update the output section with the received result
    outputSection.innerHTML = result;

    // Additional code for sending input data to the Python server if needed
    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: result })
    })
        .then(response => response.json())
        .then(data => {
            // Handle the server response if needed
        });
}