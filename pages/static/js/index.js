if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
};

function copyToClipboard(text) {
  const listener = function (event) {
    event.preventDefault();
    event.clipboardData.setData("text/plain", text);
  };
  document.addEventListener("copy", listener);
  document.execCommand("copy");
  document.removeEventListener("copy", listener);
}

[...document.querySelectorAll("a[rel~='keep-params']")].forEach(element => {
  const url = new URL(element.href);
  
  // Append current page params to the link
  new URLSearchParams(window.location.search).forEach((v, k) => url.searchParams.set(k, v));
  
  if (window.location.hostname === url.hostname) {
    // Same domain: keep relative path, append params
    element.href = url.pathname + url.search + url.hash;
  } else {
    element.href = url.toString();
  }
})

document.addEventListener("DOMContentLoaded", () => {
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll(".navbar-burger"), 0);

  $navbarBurgers.forEach(element => {
    element.addEventListener("click", () => {
      const target = element.dataset.target;
      const $target = document.getElementById(target);

      element.classList.toggle("is-active");
      $target.classList.toggle("is-active");
    });
  });

});