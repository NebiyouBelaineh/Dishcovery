$(function () {
  window.onload = function () {
    window.scrollTo(0, 0);
  };
  const bookmarkDetails = {};
  let isBookmarked = true;
  let bookmarkID = '';

  function populateModal () {
    console.log('Recipe linked clicked, Modal Open!');

    // Obtain the recipeTitle to use as a search parameter
    const recipeLink = this.parentNode;
    const recipeId = recipeLink.id;
    bookmarkID = recipeId;
    console.log('recipeId: ', recipeId);
    const recipeInfo = {
      recipeId
    };
    const recipeJson = JSON.stringify(recipeInfo);

    fetch('/get_bookmark', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: recipeJson
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((recipeContent) => {
        const source = recipeContent.source;
        const ingredients = JSON.parse(recipeContent.ingredients);
        const calories = recipeContent.calories;
        const totalTime = recipeContent.total_time;
        const tags = JSON.parse(recipeContent.tags);
        const img = recipeContent.image_link;
        const fullDetails = recipeContent.link;
        const label = recipeContent.label;

        bookmarkDetails.source = source;
        bookmarkDetails.ingredients = ingredients;
        bookmarkDetails.calories = Math.round(calories);
        bookmarkDetails.totalTime = totalTime;
        bookmarkDetails.tags = tags;
        bookmarkDetails.img = img;
        bookmarkDetails.link = fullDetails;
        bookmarkDetails.label = label;

        // Set values in the modal
        document.querySelector('.totalTime').textContent = totalTime;
        document.querySelector('.calories').textContent = Math.round(calories);

        document.querySelector('.recipe-img').setAttribute('src', img);
        document.querySelector('.label').textContent = label;
        document.querySelector('.source').textContent = source;
        document
          .querySelector('.fulldetails')
          .setAttribute('href', fullDetails);

        const healthLabels = document.querySelector('.healthLabels');
        // Clears the tags from previous tags
        healthLabels.innerHTML = '';
        if (Array.isArray(tags)) {
          tags.forEach((tag) => {
            const span = document.createElement('span');
            span.classList.add('tag');
            span.textContent = tag;
            healthLabels.appendChild(span);
          });
        }

        const ingDiv = document.createElement('div');
        const ul = document.createElement('ul');

        // console.log("ingredients: ", JSON.parse(ingredients))

        ingredients.forEach((ingredient) => {
          const li = document.createElement('li');
          const p = document.createElement('p');
          p.classList.add('ingredients-list');
          p.textContent = ingredient;
          li.appendChild(p);
          ul.appendChild(li);
        });
        ingDiv.appendChild(ul);
        document.querySelector('.ingredient').appendChild(ingDiv);
      })
      .catch((error) => {
        // Handle errors
        console.log('There was a problem with the fetch operation:', error);
      });
  }

  const clickedRecipe = document.querySelectorAll('.recipe-link');
  clickedRecipe.forEach((element) => {
    element.addEventListener('click', populateModal);
  });

  function toggleBookmark () {
    isBookmarked = !isBookmarked; // Toggle bookmark state

    if (isBookmarked) {
      // Change button text to "Remove Bookmark" if bookmarked
      bookmarkButton.textContent = 'Remove Bookmark';
      // Perform action when bookmark is added
      makeBookmark();
    } else {
      // Change button text to "Bookmark" if not bookmarked
      bookmarkButton.textContent = 'Bookmark';
      // Perform action when bookmark is removed
      removeBookmark();
    }
  }

  function makeBookmark () {
    // console.log("Bookmark button clicked");

    const recipeJSON = JSON.stringify(bookmarkDetails);
    // Sends the recipe details to save them as bookmark
    fetch('/save_bookmark', {
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
        return response.json();
        // window.location.href = "/bookmarks";
      })
      .then((response) => {
        console.log(response.message);
      })
      .catch((error) => {
        // Handle errors
        console.log('There was a problem with the fetch operation:', error);
      });
  }
  function removeBookmark () {
    // console.log("Remove Bookmark button clicked");

    const recipeInfo = {
      recipeId: bookmarkID
    };
    const recipeJSON = JSON.stringify(recipeInfo);

    // Sends the recipe details to save them as bookmark
    fetch('/delete_bookmark', {
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
        return response.json();
        // window.location.href = "/bookmarks";
      })
      .then((response) => {
        console.log(response.message);
        location.reload();
      })
      .catch((error) => {
        // Handle errors
        console.log('There was a problem with the fetch operation:', error);
      });
  }
  const bookmarkButton = document.getElementById('bookmark-btn');
  bookmarkButton.addEventListener('click', toggleBookmark);
});
