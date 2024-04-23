$(function () {
    // Function to add ingredient input
function addIngredientInput() {
    const container = document.getElementById("ingredientContainer");

    // Create label element
    const label = document.createElement("label");
    label.setAttribute("for", "ingredient");
    label.classList.add("form-label");
    label.textContent = "Ingredient:";

    // Create input element
    const input = document.createElement("input");
    input.type = "text";
    input.list = "suggestions";
    input.classList.add("form-control");
    input.placeholder = "Eggs, Tomato, Cheese, ...";
    input.required = true;

    // Create button element
    const button = document.createElement("button");
    button.type = "button";
    button.classList.add("btn", "btn-secondary", "rounded-pill");
    button.textContent = "Add";

    // Create datalist element
    const dataList = document.createElement("datalist");
    dataList.id = "suggestions";

    // Append input and button to input group
    const inputGroup = document.createElement("div");
    inputGroup.classList.add("input-group");
    inputGroup.appendChild(input);
    inputGroup.appendChild(button);
    inputGroup.appendChild(dataList);

    // Append label and input group to container
    container.appendChild(label);
    container.appendChild(inputGroup);
}

// Add event listener to the button
document.getElementById("addIngredientButton").addEventListener("click", addIngredientInput);
    
});