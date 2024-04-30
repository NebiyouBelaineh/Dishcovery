$(function () {
  function populateModal(event) {
    const filename = "/static/data/tmp/response.json";

    console.log("Recipe linked clicked, Modal Open!");

    // Obtain the recipeTitle to use as a search parameter
    const recipeLink = event.currentTarget;
    // trim() used to remove spaces from both sides of the h5 element due to formatting
    const recipeTitle = recipeLink.querySelector("h5").textContent.trim();
    console.log(recipeTitle);

    fetch(filename)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Modal Data loaded successfully");
        // console.log(data.hits)
        const recipe_list = data.hits;
        // console.log(recipe_list);
        recipe_list.forEach((element) => {
          if (element.recipe.label === recipeTitle) {
            console.log("Match Found");

            // Extract values from the response JSON file
            const source = element.recipe.source;
            const ingredients = element.recipe.ingredientLines;
            const calories = element.recipe.calories;
            const totalTime = element.recipe.totalTime;
            let tags = element.recipe.tags;
            const img = element.recipe.image;
            const fullDetails = element.recipe.url;

            console.log("source: ", source);
            console.log("ingredients: ", ingredients);
            console.log("calories: ", calories);
            console.log("totalTime: ", totalTime);
            console.log("tags: ", tags);
            console.log("img: ", img);
            console.log("fullDetails: ", fullDetails);
            console.log("label: ", recipeTitle);

            // Set values in the modal
            document.querySelector(".totalTime").textContent = totalTime;
            document.querySelector(".calories").textContent =
              Math.round(calories);

            document.querySelector(".recipe-img").setAttribute("src", img);
            document.querySelector(".label").textContent = recipeTitle;
            document.querySelector(".source").textContent = source;
            document
              .querySelector(".fulldetails")
              .setAttribute("href", fullDetails);

            const healthLabels = document.querySelector(".healthLabels");
            // Clears the tags from previous tags
            healthLabels.innerHTML = "";
            if (Array.isArray(tags)) {
              tags.forEach((tag) => {
                const span = document.createElement("span");
                span.classList.add("tag");
                span.textContent = tag;
                healthLabels.appendChild(span);
              });
            }

            const ingDiv = document.createElement("div");
            const ul = document.createElement("ul");

            ingredients.forEach((ingredient) => {
              const li = document.createElement("li");
              const p = document.createElement("p");
              p.classList.add("ingredients-list");
              p.textContent = ingredient;
              li.appendChild(p);
              ul.appendChild(li);
            });
            ingDiv.appendChild(ul);
            document.querySelector(".ingredient").appendChild(ingDiv);
          }
        });
      })
      .catch((error) => {
        console.error("There was a problem fetching the file:", error);
      });
  }
  const clickedRecipe = document.querySelectorAll(".recipe-link");
  clickedRecipe.forEach((element) => {
    element.addEventListener("click", populateModal);
  });
});
