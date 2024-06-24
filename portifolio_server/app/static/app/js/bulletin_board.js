var styleSheet=document.styleSheets[0],keyframes=`@keyframes slideAnimation {
    from {
        transform: translateX(100%);
      }
      to {
        transform: translateX(-100%);
      }
}`;styleSheet.insertRule(keyframes,styleSheet.cssRules.length);var animatedDiv=document.getElementById("animatedDiv");animatedDiv.style.animation="slideAnimation 2s ease-in-out forwards";