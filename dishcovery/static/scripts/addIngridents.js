let addedPrior = false;
$(function () {
  function capitalizeFirstLetter(str) {
    if (str.length === 0) {
      return str;
    }
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  function addIngredientInput() {
    console.log("Add button clicked!");
    const ingrident = document.getElementById("ingredients");
    const inputText = ingrident.value;
    // console.log(inputText);
    const container = document.querySelector(".ingredientContainer");

    const selectedContainer = document.createElement("div");

    if (!addedPrior) {
      selectedContainer.innerHTML = "Selected Ingredients: ";
    }

    selectedContainer.classList.add("selectedIngredients");

    const selectedIngrident = document.createElement("p");
    selectedIngrident.setAttribute("style", "display: inline");
    selectedIngrident.classList.add("ingridentText");
    const span = document.createElement("span");
    span.classList = "badge rounded-pill bg-secondary selected-ingredients";
    span.innerHTML = `${capitalizeFirstLetter(inputText)}`;
    selectedIngrident.appendChild(span);
    selectedContainer.appendChild(selectedIngrident);
    container.appendChild(selectedContainer);
    ingrident.value = "";
    addedPrior = true;
    document.getElementById("ingredients").focus();
  }

  // Add event listener to the button
  document
    .getElementById("addIngredientButton")
    .addEventListener("click", addIngredientInput);
});
