document.addEventListener("DOMContentLoaded", function () {
    const updateLinks = document.querySelectorAll("a[href*='?update=']");
    const itemField = document.getElementById("item");
    const priceField = document.getElementById("price");
    const addressField = document.getElementById("address");
    const itemIdField = document.getElementById("item_id");

    updateLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();

            const url = new URL(link.href);
            const itemId = url.searchParams.get("update");

            // Find the row where the item info exists
            const row = link.closest("tr");
            const itemName = row.children[0].textContent.trim();
            const itemPrice = row.children[1].textContent.trim();
            const itemAddress = row.children[2].textContent.trim();

            // Fill form fields
            itemField.value = itemName;
            priceField.value = itemPrice;
            addressField.value = itemAddress;
            itemIdField.value = itemId;

            // Optionally change button label (if dynamic behavior is preferred)
            const submitBtn = document.querySelector("form button[type='submit']");
            submitBtn.textContent = "Update Item";
        });
    });
});
