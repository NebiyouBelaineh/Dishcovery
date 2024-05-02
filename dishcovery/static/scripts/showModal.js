$(function () {
  window.onload = function () {
    window.scrollTo(0, 0);
  };
  const recipeContent = {};

  const tags = document.querySelector("#tagsContent");
  const cursor_tag = document.querySelector("#showTags");
  cursor_tag.addEventListener("click", function (e) {
    if (this.children[0].getAttribute("name") === "chevron-up-outline") {
      this.children[0].setAttribute("name", "chevron-down-outline");
    } else {
      this.children[0].setAttribute("name", "chevron-up-outline");
    }
  });
  $("#tagsContent").hide();
  $("#showTags").click(function () {
    $("#tagsContent").slideToggle(300);
  });

  // document.getElementById("pdf-btn").addEventListener("click", saveToPDF);
  $("#pdf-btn").click(function () {
    $("#modal-section").printThis();
  });

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
            const tags = element.recipe.tags;
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

            // Save values to recipeContent dict
            recipeContent.source = source;
            recipeContent.ingredients = ingredients;
            recipeContent.calories = Math.round(calories);
            recipeContent.totalTime = totalTime;
            recipeContent.tags = tags;
            recipeContent.img = img;
            recipeContent.link = fullDetails;
            recipeContent.label = recipeTitle;

            // console.log(recipeContent)

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

  function makeBookmark() {
    console.log("Bookmark button clicked");

    const recipeJSON = JSON.stringify(recipeContent);
    // Sends the recipe details to save them as bookmark
    fetch("/save_bookmarks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: recipeJSON,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        // window.location.href = "/bookmarks";
      })
      .catch((error) => {
        // Handle errors
        console.log("There was a problem with the fetch operation:", error);
      });
  }
  // $('#bookmark-btn').click(makeBookmark);
  document
    .getElementById("bookmark-btn")
    .addEventListener("click", makeBookmark);
});
