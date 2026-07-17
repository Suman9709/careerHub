const searchInput = document.getElementById("search-input");
const jobCards = document.querySelectorAll(".job-card");

searchInput.addEventListener("input", function () {
  const query = searchInput.value.toLowerCase();
  let matches = 0;

  jobCards.forEach(function (card) {
    const jobDetails = card.textContent.toLowerCase();
    const isMatch = jobDetails.includes(query);

    card.style.display = isMatch ? "block" : "none";
  });


});
