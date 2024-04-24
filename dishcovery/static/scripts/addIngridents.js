$(function () {
  // Function to add ingredient input

  function addIngredientInput() {
    console.log("Add button clicked!");
    const ingrident = document.getElementById("ingridents");
    const inputText = ingrident.value;
    console.log(inputText);
    const container = document.querySelector(".ingredientContainer");
    const selectedIngrident = document.createElement("p");
    selectedIngrident.setAttribute("style", "display: inline");
    const span = document.createElement("span");
    span.classList = "badge rounded-pill bg-secondary selected-ingridents";
    span.innerHTML = `${inputText}`;
    selectedIngrident.appendChild(span);
    container.appendChild(selectedIngrident);
    ingrident.value = "";
  }

  // Add event listener to the button
  document
    .getElementById("addIngredientButton")
    .addEventListener("click", addIngredientInput);
});
