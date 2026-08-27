/* =========================================================
   MEDIMATCH - GLOBAL JAVASCRIPT
   Responsive navigation & interactions
   ========================================================= */

document.addEventListener("DOMContentLoaded", () => {

    const menuButton =
        document.getElementById("mobile-menu-button");

    const mobileMenu =
        document.getElementById("mobile-menu");


    if (!menuButton || !mobileMenu) {
        return;
    }


    // =====================================================
    // TOGGLE MENU
    // =====================================================

    function toggleMenu() {

        const isHidden =
            mobileMenu.classList.contains("hidden");

        if (isHidden) {

            mobileMenu.classList.remove("hidden");
            menuButton.setAttribute("aria-expanded", "true");

        } else {

            mobileMenu.classList.add("hidden");
            menuButton.setAttribute("aria-expanded", "false");

        }

    }


    function closeMenu() {

        if (!mobileMenu.classList.contains("hidden")) {

            mobileMenu.classList.add("hidden");
            menuButton.setAttribute("aria-expanded", "false");

        }

    }


    // Button click
    menuButton.addEventListener("click", (event) => {

        event.stopPropagation();
        toggleMenu();

    });


    // Close when clicking outside
    document.addEventListener("click", (event) => {

        if (
            !mobileMenu.contains(event.target) &&
            !menuButton.contains(event.target)
        ) {
            closeMenu();
        }

    });


    // Close on Escape key
    document.addEventListener("keydown", (event) => {

        if (event.key === "Escape") {
            closeMenu();
        }

    });


    // Close automatically when resizing back to desktop screen (> 768px)
    window.addEventListener("resize", () => {

        if (window.innerWidth >= 768) {
            closeMenu();
        }

    });

});