
    // Agrega eventos a los botones del carrusel y asegura que no se salgan de su contenedor
    var carouselContainer = document.querySelector('.carousel');
    var previousButton = document.querySelector('.carousel-control-prev');
    var nextButton = document.querySelector('.carousel-control-next');
    var carousel = document.querySelector('#carouselExampleIndicators');
    var carouselItems = carousel.querySelectorAll('.carousel-item');
    var totalCarouselItems = carouselItems.length;

    function cycleCarousel(direction) {
        var currentIndex = Array.from(carouselItems).findIndex(item => item.classList.contains('active'));
        var newIndex = (currentIndex + direction + totalCarouselItems) % totalCarouselItems;

        carouselItems[currentIndex].classList.remove('active');
        carouselItems[newIndex].classList.add('active');

        carousel.classList.remove('slide');
        void carousel.offsetWidth; // Forza al navegador a renderizar el cambio
        carousel.classList.add('slide');
    }

    previousButton.addEventListener('click', cycleCarousel.bind(null, -1));
    nextButton.addEventListener('click', cycleCarousel.bind(null, 1));

    carouselContainer.addEventListener('click', function(event) {
        if (event.target === carouselContainer) {
            event.stopPropagation();
        }
    }, {passive: true, capture: true});

    previousButton.addEventListener('click', function(event) {
        event.stopPropagation();
    }, {passive: true, capture: true});

    nextButton.addEventListener('click', function(event) {
        event.stopPropagation();
    }, {passive: true, capture: true});

    // Comprime las imágenes que se muestran en el carrusel
    var carouselImages = document.querySelectorAll('#carouselExampleIndicators img');
    carouselImages.forEach(img => {
        var compressedUrl = img.src.replace(/static\/images\/Cover\/(.*)/, 'static/images/Cover/$1?compress');
        img.src = compressedUrl;
    });

    document.addEventListener('DOMContentLoaded', () => {
        const logo = document.querySelector('.logo-lilicafe');
        const image = document.createElement('img');
        image.src = logo.dataset.img;
        logo.appendChild(image);
    });

