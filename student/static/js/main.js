// =========================================
// CLOPLO - MAIN JAVASCRIPT
// =========================================


// =========================================
// 1. DROPDOWN MENUS
// =========================================

const dropdownButtons =
 document.querySelectorAll(".dropdown-toggle");


dropdownButtons.forEach(function (button) {

 button.addEventListener("click", function () {

 const group =
 button.closest(".nav-group");


 // Close other dropdowns
 document
 .querySelectorAll(".nav-group")
 .forEach(function (otherGroup) {

 if (otherGroup !== group) {

 otherGroup.classList.remove("open");

 }

 });


 // Toggle current dropdown
 group.classList.toggle("open");

 });

});


// =========================================
// 2. MOBILE SIDEBAR
// =========================================

const menuButton =
 document.getElementById("menuButton");

const sidebar =
 document.getElementById("sidebar");


if (menuButton && sidebar) {

 menuButton.addEventListener("click", function () {

 sidebar.classList.toggle("open");

 });

}


// =========================================
// 3. DARK MODE
// =========================================

const themeButton =
 document.getElementById("themeButton");


if (themeButton) {

 themeButton.addEventListener("click", function () {

 document.body.classList.toggle("dark");


 // Save user's preference
 if (document.body.classList.contains("dark")) {

 localStorage.setItem(
 "cloplo-theme",
 "dark"
 );

 } else {

 localStorage.setItem(
 "cloplo-theme",
 "light"
 );

 }

 });

}


// =========================================
// 4. LOAD SAVED THEME
// =========================================

const savedTheme =
 localStorage.getItem("cloplo-theme");


if (savedTheme === "dark") {

 document.body.classList.add("dark");

}


// =========================================
// 5. CLOSE SIDEBAR WHEN CLICKING OUTSIDE
// =========================================

document.addEventListener("click", function (event) {

 if (!sidebar || !menuButton) {
 return;
 }


 const clickedInsideSidebar =
 sidebar.contains(event.target);

 const clickedMenuButton =
 menuButton.contains(event.target);


 if (
 !clickedInsideSidebar &&
 !clickedMenuButton
 ) {

 sidebar.classList.remove("open");

 }

});