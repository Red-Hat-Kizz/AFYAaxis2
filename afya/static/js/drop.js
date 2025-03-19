document.addEventListener("DOMContentLoaded", function() {
    const dropdownBtns = document.querySelectorAll('.dropdown-btn');

    dropdownBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();

            // Close all other open submenus
            dropdownBtns.forEach(otherBtn => {
                if (otherBtn !== btn) {
                    const otherDropdown = otherBtn.closest('.dropdown');
                    const otherIcon = otherBtn.querySelector('.dropdown-icon');

                    otherDropdown.classList.remove('active');
                    otherIcon.style.transform = 'rotate(-90deg)'; // Reset icon rotation
                }
            });

            // Toggle the clicked dropdown
            const dropdown = btn.closest('.dropdown');
            const dropdownIcon = btn.querySelector('.dropdown-icon');

            dropdown.classList.toggle('active');

            // Rotate the dropdown icon
            if (dropdown.classList.contains('active')) {
                dropdownIcon.style.transform = 'rotate(0deg)'; // Rotate 90 degrees when open
            } else {
                dropdownIcon.style.transform = 'rotate(-90deg)'; // Rotate -90 degrees when closed
            }
        });
    });
});


var swiper = new Swiper(".mySwiper", {
  spaceBetween: 30,
  centeredSlides: true,
  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});

const opensidebar = document.getElementById('opensidebar').addEventListener('click',function(){
    var sidebarrepo = document.getElementById('sidebarrepo');

    sidebarrepo.style.right = "0"
})

const closesidebar = document.getElementById('closesidebar').addEventListener('click',function(){
    var sidebarrepo = document.getElementById('sidebarrepo');

    sidebarrepo.style.right = "-100%"
})

