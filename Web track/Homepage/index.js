document.getElementById("hidden").addEventListener("click", showHidden);

function showHidden() {
  text = document.querySelector("#btn-text").innerHTML;
  if (text !== "Shrink me") {
    document.querySelector("#btn-text").innerHTML = "Shrink me";
  } else {
    document.querySelector("#btn-text").innerHTML =
      "Wanna find more? - Click me";
  }

  let hidden = document.getElementById("index-hidden-wrapper");
  //  getElementByClassName returns a Nodelist -> using index to call it if theres is only 1 element.
  if (hidden.style.visibility === "visible") {
    hidden.style.visibility = "hidden";
  } else {
    hidden.style.visibility = "visible";
  }
}
