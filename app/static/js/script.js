/* =========================================================
MEDIMATCH - GLOBAL JAVASCRIPT
Responsive navigation & interactions
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

```
const menuButton =
    document.getElementById("mobile-menu-button");

const mobileMenu =
    document.getElementById("mobile-menu");


if (!menuButton || !mobileMenu) {
    return;
}


const mobileLinks =
    mobileMenu.querySelectorAll(".mobile-nav-link");


// =====================================================
// MENU STATE
// =====================================================

function isMenuOpen() {

    return !mobileMenu.classList.contains("hidden");

}


// =====================================================
// OPEN MENU
// =====================================================

function openMenu() {

    mobileMenu.classList.remove("hidden");

    menuButton.setAttribute(
        "aria-expanded",
        "true"
    );

    menuButton.setAttribute(
        "aria-label",
        "Close navigation menu"
    );

}


// =====================================================
// CLOSE MENU
// =====================================================

function closeMenu() {

    mobileMenu.classList.add("hidden");

    menuButton.setAttribute(
        "aria-expanded",
        "false"
    );

    menuButton.setAttribute(
        "aria-label",
        "Open navigation menu"
    );

}


// =====================================================
// TOGGLE MENU
// =====================================================

function toggleMenu() {

    if (isMenuOpen()) {
        closeMenu();
    } else {
        openMenu();
    }

}


// =====================================================
// HAMBURGER BUTTON
// =====================================================

menuButton.addEventListener("click", (event) => {

    event.stopPropagation();

    toggleMenu();

});


// =====================================================
// CLOSE WHEN CLICKING OUTSIDE
// =====================================================

document.addEventListener("click", (event) => {

    if (!isMenuOpen()) {
        return;
    }

    if (
        !mobileMenu.contains(event.target) &&
        !menuButton.contains(event.target)
    ) {

        closeMenu();

    }

});


// =====================================================
// CLOSE AFTER CLICKING A MOBILE LINK
// =====================================================

mobileLinks.forEach((link) => {

    link.addEventListener("click", () => {

        closeMenu();

    });

});


// =====================================================
// ESCAPE KEY
// =====================================================

document.addEventListener("keydown", (event) => {

    if (event.key === "Escape" && isMenuOpen()) {

        closeMenu();

        menuButton.focus();

    }

});


// =====================================================
// CLOSE ON DESKTOP RESIZE
// =====================================================

window.addEventListener("resize", () => {

    if (window.innerWidth >= 768) {

        closeMenu();

    }

});
```

});
