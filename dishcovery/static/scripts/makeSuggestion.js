$(function () {
  $(document).keypress(function (event) {// Disable enter/return key
    if (event.which == "13") {
      event.preventDefault();
    }
  });
  const inputField = document.getElementById("ingredients");
  const dataList = document.getElementById("suggestions");
  
  const filename = "/static/data/food_list.json";
  // const suggestions = ["chicken", "onion", "beef", "fish", "bread", "corn"];
  let suggestions = [];

  fetch(filename)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Data loaded successfully')
            suggestions = data;
            inputField.addEventListener("input", makeSuggestion);
        })
        .catch(error => {
            console.error('There was a problem fetching the file:', error);
        });

  function makeSuggestion() {
    const inputText = this.value.toLowerCase();
    const filteredSuggestions = suggestions.filter((suggestion) =>
      suggestion.toLowerCase().startsWith(inputText)
    );
    dataList.innerHTML = "";

    filteredSuggestions.forEach((suggestion) => {
      const option = document.createElement("option");
      option.value = suggestion;
      dataList.appendChild(option);
    });
  }
});
