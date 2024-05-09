var styleSheet = document.styleSheets[0];
  
// Define the keyframes
var keyframes = `@keyframes slideAnimation {
    from {
        transform: translateX(100%);
      }
      to {
        transform: translateX(-100%);
      }
}`;


// var logoImages = document.querySelectorAll('.logos-container .logo');

// // Loop through each image and do something
// logoImages.forEach(function(image) {
//   console.log(image.src); // Example: Print the source of each image
// });

// Append the keyframes to the stylesheet
styleSheet.insertRule(keyframes, styleSheet.cssRules.length);

// Apply the animation to the div
var animatedDiv = document.getElementById("animatedDiv");
animatedDiv.style.animation = "slideAnimation 2s ease-in-out forwards";
