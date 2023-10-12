//Link embedding
function showLinkPopup() {
  document.getElementById("link-popup").style.display = "block";
}

function embedLink() {
  var linkUrl = document.getElementById("link-url").value;
  var questionBox = document.getElementById("question");
  questionBox.value += linkUrl;
  document.getElementById("link-popup").style.display = "none";
}