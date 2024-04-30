$(function () {
  const ingredientsList = [];
  function removePromptStr (str) {
    if (str.length === 0) {
      return str;
    }
    return str.replace('Selected Ingredients: ', '');
  }
  function collectRecipeDetails () { // Collects the recipe details from the DOM
    const ingredients = document.querySelectorAll('.selectedIngredients');
    let cuisines = document.getElementById('cuisines').value;
    let meals = document.getElementById('meals').value;
    let dishes = document.getElementById('dishes').value;

    // console.log(ingredients)
    // After collecting all ingredients into an array, this will remove the prompt string
    ingredients.forEach((element) => {
      ingredientsList.push(removePromptStr(element.textContent));
      //   console.log(removePromptStr(element.textContent));
    });

    cuisines = cuisines.replace('(Default) - Any', '');
    dishes = dishes.replace('(Default) - Any', '');
    meals = meals.replace('(Default) - Any', '');

    const formDataObject = {
      ingredients: ingredientsList,
      cuisineType: cuisines,
      mealType: meals,
      dishType: dishes
    };

    console.log(formDataObject);
    const recipeJSON = JSON.stringify(formDataObject);
    console.log(recipeJSON);

    fetch('/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: recipeJSON
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        // Redirect to the /results route after successful POST request
        window.location.href = '/results';
      })
      .catch((error) => {
        // Handle errors
        console.error('There was a problem with the fetch operation:', error);
      });
  }

  document
    .getElementById('sumbitRecipeButton')
    .addEventListener('click', collectRecipeDetails);
});
