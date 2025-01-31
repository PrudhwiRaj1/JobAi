document.addEventListener("DOMContentLoaded", function () {
  const listItems = document.querySelectorAll("#menu li");

  listItems.forEach(item => {
      item.addEventListener("click", function () {
          // Remove highlight from all items
          listItems.forEach(li => li.classList.remove("highlight"));

          // Add highlight to the clicked item
          this.classList.add("highlight");
      });
    });
});