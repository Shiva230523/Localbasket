document.addEventListener('DOMContentLoaded', function() {
    const toast = document.getElementById('toast');
    if (toast && toast.innerHTML.trim() !== "") {
        toast.style.display = 'block';
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => {
                toast.style.display = 'none';
            }, 300);
        }, 3000);
    }

    // You can add more JavaScript functionality here, e.g.,
    // - Handling the "Edit Avatar" button click
    // - Implementing client-side form validation
});