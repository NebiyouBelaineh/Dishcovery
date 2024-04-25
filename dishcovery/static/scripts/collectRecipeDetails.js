let ingredientsList = [];
$(function () {
  function removePromptStr(str) {
    if (str.length === 0) {
      return str;
    }
    return str.replace("Selected Ingredients: ", "");
  }
  function collectRecipeDetails() {
    const ingredients = document.querySelectorAll(".selectedIngredients");
    const cuisines = document.getElementById("cuisines").value
    const meals = document.getElementById("meals").value
    const dishes = document.getElementById("dishes").value

    // console.log(ingredients)
    ingredients.forEach((element) => {
      ingredientsList.push(removePromptStr(element.textContent));
      //   console.log(removePromptStr(element.textContent));
    });
    console.log(ingredientsList);
    console.log(cuisines);
    console.log(meals);
    console.log(dishes);

  }
  document
    .getElementById("sumbitRecipeButton")
    .addEventListener("click", collectRecipeDetails);
});
