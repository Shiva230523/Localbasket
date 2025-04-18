
// document.addEventListener("DOMContentLoaded", function () {
//     const searchInput = document.getElementById("searchInput");

//     searchInput.addEventListener("input", function () {
//         const value = searchInput.value.trim();

//         // If input is cleared, reload page without search param
//         if (value === "") {
//             window.location.href = "{% url 'buyer:buyer_home' %}";
//         }
//     });
// });

document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const searchForm = document.getElementById("searchForm");

    searchInput.addEventListener("input", function () {
        if (searchInput.value.trim() === "") {
            // Redirect to original page with no query params
            window.location.href = searchForm.getAttribute("action");
        }
    });
});