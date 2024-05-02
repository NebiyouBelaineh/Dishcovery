$(function () {
  window.onload = function () {
    window.scrollTo(0, 0);
  };
  const recipeContent = {};

  const tags = document.querySelector('#tagsContent');
  const cursor_tag = document.querySelector('#showTags');
  cursor_tag.addEventListener('click', function (e) {
    if (this.children[0].getAttribute('name') === 'chevron-up-outline') {
      this.children[0].setAttribute('name', 'chevron-down-outline');
    } else {
      this.children[0].setAttribute('name', 'chevron-up-outline');
    }
  });
  $('#tagsContent').hide();
  $('#showTags').click(function () {
    $('#tagsContent').slideToggle(300);
  });

  // document.getElementById("pdf-btn").addEventListener("click", saveToPDF);
  $('#pdf-btn').click(function () {
    $('#modal-section').printThis();
  });

  function populateModal (event) {
    console.log('Recipe linked clicked, Modal Open!');

    // Obtain the recipeTitle to use as a search parameter
    const recipeLink = event.currentTarget;
    // trim() used to remove spaces from both sides of the h5 element due to formatting
    // const recipeTitle = recipeLink.querySelector("h5").textContent.trim();
    const recipeId = recipeLink.getAttribute('id');
    console.log(recipeId);

    const recipeInfo = {
      recipeId
    };
    const recipeJson = JSON.stringify(recipeInfo);

    fetch('/get_recipe', {
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
      .then((hit) => {
        if (hit == {}) {
          console.log('Recipe Details is empty');
        } else {
          const source = hit.source;
          const ingredients = hit.ingredientLines;
          const calories = hit.calories;
          const totalTime = hit.totalTime;
          const tags = hit.tags;
          const img = hit.image;
          const fullDetails = hit.url;
          const label = hit.label;

          console.log('source: ', source);
          console.log('ingredients: ', ingredients);
          console.log('calories: ', calories);
          console.log('totalTime: ', totalTime);
          console.log('tags: ', tags);
          console.log('img: ', img);
          console.log('fullDetails: ', fullDetails);
          console.log('label: ', label);

          // Save values to recipeContent dict
          recipeContent.source = source;
          recipeContent.ingredients = ingredients;
          recipeContent.calories = Math.round(calories);
          recipeContent.totalTime = totalTime;
          recipeContent.tags = tags;
          recipeContent.img = img;
          recipeContent.link = fullDetails;
          recipeContent.label = label;

          // console.log(recipeContent)

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
        }
      })
      .catch((error) => {
        console.error('There was a problem fetching the file:', error);
      });
  }

  function makeBookmark () {
    console.log('Bookmark button clicked');

    const recipeJSON = JSON.stringify(recipeContent);
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
        console.log(response);
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
  document
    .getElementById('bookmark-btn')
    .addEventListener('click', makeBookmark);
});
