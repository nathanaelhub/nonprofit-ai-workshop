// Slides: arrow keys, space or click to move; N shows speaker notes; the URL hash keeps your place.
(function () {
  const slides = Array.from(document.querySelectorAll(".deck .slide"));
  if (!slides.length) return;
  document.documentElement.classList.add("js");
  let i = Math.max(0, slides.findIndex((s) => "#" + s.id === location.hash));

  function show(n) {
    i = Math.min(slides.length - 1, Math.max(0, n));
    slides.forEach((s, k) => s.classList.toggle("current", k === i));
    history.replaceState(null, "", "#" + slides[i].id);
    help.textContent = `${i + 1} / ${slides.length} · arrows to move · N for notes`;
  }

  const help = document.createElement("div");
  help.className = "deck-help";
  document.body.appendChild(help);

  document.addEventListener("keydown", (e) => {
    if (["ArrowRight", "PageDown", " "].includes(e.key)) { e.preventDefault(); show(i + 1); }
    else if (["ArrowLeft", "PageUp"].includes(e.key)) { e.preventDefault(); show(i - 1); }
    else if (e.key === "Home") show(0);
    else if (e.key === "End") show(slides.length - 1);
    else if (e.key.toLowerCase() === "n") document.body.classList.toggle("show-notes");
  });
  document.querySelector(".deck").addEventListener("click", (e) => {
    if (e.target.closest("a")) return;
    show(e.clientX > window.innerWidth / 3 ? i + 1 : i - 1);
  });
  show(i);
})();
