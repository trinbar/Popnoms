'use strict';

//create like button that changes the like button to
//highlight pink when clicked, and gray when unclicked
let likeButton = document.querySelector("#likeButton");

likeButton.addEventListener("click", function () {
  if (likeButton.innerText === "<3") {
    likeButton.innerText = "unlike";
  } else {
    likeButton.innerText = "<3";
  }
});
