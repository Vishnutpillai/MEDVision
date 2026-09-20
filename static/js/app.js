/* =========================================
   MEDVISION AI
   Frontend JavaScript
========================================= */

document.addEventListener("DOMContentLoaded", function () {

    console.log("MedVision AI frontend initialized.");

    initializeMobileSidebar();
    initializeNotifications();
    initializeLoadingButtons();
    initializeFileUploads();
    initializeForms();

});


/* =========================================
   MOBILE SIDEBAR
========================================= */

function initializeMobileSidebar() {

    const sidebar = document.querySelector(".sidebar");
    const mobileMenu = document.querySelector(".mobile-menu");

    if (!sidebar || !mobileMenu) {
        return;
    }

    mobileMenu.addEventListener("click", function () {

        sidebar.classList.toggle("show");

    });


    /*
     * Close sidebar when clicking
     * outside the sidebar.
     */

    document.addEventListener("click", function (event) {

        const clickedInsideSidebar =
            sidebar.contains(event.target);

        const clickedMenu =
            mobileMenu.contains(event.target);

        if (
            !clickedInsideSidebar &&
            !clickedMenu &&
            sidebar.classList.contains("show")
        ) {

            sidebar.classList.remove("show");

        }

    });


    /*
     * Close sidebar after
     * selecting a navigation item.
     */

    const navigationLinks =
        sidebar.querySelectorAll(".nav-link");

    navigationLinks.forEach(function (link) {

        link.addEventListener("click", function () {

            sidebar.classList.remove("show");

        });

    });

}


/* =========================================
   NOTIFICATIONS
========================================= */

function initializeNotifications() {

    const notificationButton =
        document.querySelector(".icon-button");

    if (!notificationButton) {
        return;
    }

    notificationButton.addEventListener(
        "click",
        function () {

            showToast(
                "No new notifications.",
                "info"
            );

        }
    );

}


/* =========================================
   LOADING BUTTONS
========================================= */

function initializeLoadingButtons() {

    const loadingButtons =
        document.querySelectorAll(
            "[data-loading]"
        );

    loadingButtons.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                const originalText =
                    button.innerHTML;

                button.disabled = true;

                button.innerHTML = `
                    <span
                        class="spinner-border spinner-border-sm me-2"
                        role="status">
                    </span>

                    Processing...
                `;


                /*
                 * Demo delay only.
                 *
                 * Real API requests will
                 * replace this later.
                 */

                setTimeout(function () {

                    button.disabled = false;

                    button.innerHTML =
                        originalText;

                }, 1500);

            }
        );

    });

}


/* =========================================
   FILE UPLOADS
========================================= */

function initializeFileUploads() {

    const fileInputs =
        document.querySelectorAll(
            'input[type="file"]'
        );


    fileInputs.forEach(function (input) {

        input.addEventListener(
            "change",
            function () {

                const file =
                    input.files[0];

                if (!file) {
                    return;
                }


                /*
                 * File size validation
                 *
                 * Current demo limit:
                 * 10 MB
                 */

                const maxSize =
                    10 * 1024 * 1024;


                if (file.size > maxSize) {

                    showToast(
                        "File size must be below 10 MB.",
                        "error"
                    );

                    input.value = "";

                    return;

                }


                /*
                 * Show selected file.
                 */

                const fileNameElement =
                    document.querySelector(
                        `[data-file-name="${input.id}"]`
                    );


                if (fileNameElement) {

                    fileNameElement.textContent =
                        file.name;

                }


                showToast(
                    `${file.name} selected successfully.`,
                    "success"
                );

            }
        );

    });

}


/* =========================================
   FORM VALIDATION
========================================= */

function initializeForms() {

    const forms =
        document.querySelectorAll(
            "form[data-validate]"
        );


    forms.forEach(function (form) {

        form.addEventListener(
            "submit",
            function (event) {

                if (!form.checkValidity()) {

                    event.preventDefault();

                    event.stopPropagation();

                    showToast(
                        "Please complete the required fields.",
                        "error"
                    );

                }

                form.classList.add(
                    "was-validated"
                );

            }
        );

    });

}


/* =========================================
   TOAST NOTIFICATION
========================================= */

function showToast(message, type = "info") {

    let container =
        document.querySelector(
            ".toast-container-custom"
        );


    /*
     * Create toast container
     * if it doesn't exist.
     */

    if (!container) {

        container =
            document.createElement("div");

        container.className =
            "toast-container-custom";

        document.body.appendChild(
            container
        );

    }


    const toast =
        document.createElement("div");


    toast.className =
        `custom-toast toast-${type}`;


    let icon =
        "bi-info-circle";


    if (type === "success") {
        icon = "bi-check-circle";
    }

    if (type === "error") {
        icon = "bi-exclamation-circle";
    }

    if (type === "warning") {
        icon = "bi-exclamation-triangle";
    }


    toast.innerHTML = `

        <i class="bi ${icon}"></i>

        <span>${message}</span>

        <button
            type="button"
            class="toast-close">

            <i class="bi bi-x"></i>

        </button>

    `;


    container.appendChild(toast);


    /*
     * Close button.
     */

    const closeButton =
        toast.querySelector(
            ".toast-close"
        );


    closeButton.addEventListener(
        "click",
        function () {

            removeToast(toast);

        }
    );


    /*
     * Automatically remove.
     */

    setTimeout(function () {

        removeToast(toast);

    }, 3500);

}


/* =========================================
   REMOVE TOAST
========================================= */

function removeToast(toast) {

    toast.classList.add("toast-hide");

    setTimeout(function () {

        toast.remove();

    }, 250);

}