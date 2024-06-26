let addedPrior = false;
$(function () {
  // Scroll page to top when reloaded
  window.onload = function () {
    window.scrollTo(0, 0);
  };
  function capitalizeFirstLetter (str) {
    if (str.length === 0) {
      return str;
    }
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  function addIngredientInput () {
    console.log('Add button clicked!');
    const ingrident = document.getElementById('ingredients');
    const inputText = ingrident.value;
    let boolAddedBefore = false;
    const ingredients = document.querySelectorAll('.selectedIngredients');

    ingredients.forEach((element) => {
      const inputBefore = element.textContent
        .trim()
        .replace('x', '')
        .replace(' ', '')
        .toLowerCase();
      // console.log("inputBefore:", inputBefore, inputBefore.length);
      // console.log("inputText:", inputText, inputText.length)

      if (inputBefore === inputText) {
        boolAddedBefore = true;
        console.log('boolAddedBefore: ', boolAddedBefore);
      }
    });

    if (inputText !== '' && !boolAddedBefore) {
      // If no text inside the input, nothing happens
      // console.log(inputText);
      const container = document.querySelector('.ingredientContainer');

      const selectedContainer = document.createElement('div');

      if (!addedPrior) {
        // Create Prompt only the first time
        const preSelectedContainer = document.createElement('div');
        preSelectedContainer.setAttribute('style', 'display: inline');
        preSelectedContainer.innerHTML = 'Selected Ingredients: ';
        container.appendChild(preSelectedContainer);
      }

      selectedContainer.classList.add('selectedIngredients');

      const selectedIngrident = document.createElement('p');
      selectedIngrident.setAttribute('style', 'display: inline');
      selectedIngrident.classList.add('ingridentText');
      const span = document.createElement('span');
      span.classList = 'badge rounded-pill bg-secondary selected-ingredients';
      span.innerHTML = `${capitalizeFirstLetter(inputText)}`;

      // Add remove button for ingredients added
      const removeSelected = document.createElement('button');
      removeSelected.setAttribute('type', 'button');
      removeSelected.classList = 'badge rounded-pill bg-dark remove-btn';
      removeSelected.innerHTML = ' x ';

      selectedIngrident.appendChild(span);
      selectedContainer.appendChild(selectedIngrident);
      selectedContainer.appendChild(removeSelected);
      removeSelected.addEventListener('click', removeIngredient);

      container.appendChild(selectedContainer);

      // Reset/Clear the value of the input box
      ingrident.value = '';
      addedPrior = true;
      document.getElementById('ingredients').focus();
    }
    document.getElementById('ingredients').focus();
  }

  function removeIngredient (event) {
    // event.preventDefault();
    console.log('Remove ingredient button clicked!');
    const parentDiv = event.target.parentNode;

    if (parentDiv) {
      parentDiv.remove();
    }
  }

  // Add event listener to the button
  document
    .getElementById('addIngredientButton')
    .addEventListener('click', addIngredientInput);
});
