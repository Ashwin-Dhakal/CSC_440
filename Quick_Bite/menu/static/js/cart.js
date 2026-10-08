(function () {
    var MAX_CART_QUANTITY = 20;

    function parseQuantity(value) {
        var quantity = parseInt(value, 10);
        if (!Number.isInteger(quantity) || quantity < 1 || quantity > MAX_CART_QUANTITY) {
            return null;
        }
        return quantity;
    }

    document.querySelectorAll('[data-cart-quantity]').forEach(function (root) {
        var input = root.querySelector('[data-qty-input]');
        var updateForm = root.querySelector('[data-qty-update-form]');
        var decreaseForm = root.querySelector('[data-qty-decrease-form]');
        var increaseForm = root.querySelector('[data-qty-increase-form]');

        if (!input || !updateForm) {
            return;
        }

        root.classList.add('cart-quantity--enhanced');

        if (increaseForm) {
            increaseForm.addEventListener('submit', function (event) {
                event.preventDefault();
                var current = parseQuantity(input.value) || 1;
                if (current >= MAX_CART_QUANTITY) {
                    input.value = String(MAX_CART_QUANTITY);
                } else {
                    input.value = String(current + 1);
                }
                if (typeof updateForm.requestSubmit === 'function') {
                    updateForm.requestSubmit();
                } else {
                    updateForm.submit();
                }
            });
        }

        if (decreaseForm) {
            decreaseForm.addEventListener('submit', function (event) {
                var current = parseQuantity(input.value);
                if (current === null || current <= 1) {
                    // Let the decrease form remove the line (qty 1 -> gone).
                    return;
                }
                event.preventDefault();
                input.value = String(current - 1);
                if (typeof updateForm.requestSubmit === 'function') {
                    updateForm.requestSubmit();
                } else {
                    updateForm.submit();
                }
            });
        }
    });
})();
