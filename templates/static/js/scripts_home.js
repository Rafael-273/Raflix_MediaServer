// responsivo

const responsiveCarousel = document.querySelector('.js-carousel--responsive')

new Glider(responsiveCarousel, {
    slidesToShow: 2.68,
    slidesToScroll: 2.68,
    draggable: true,
    dots: '.js-carousel--responsive-dots' ,
    arrows: {
        prev: ".js-carousel--responsive-prev",
        next: ".js-carousel--responsive-next"
    },
    scrollLock: true,
    responsive: [
        {
            breakpoint: 2500,
            settings: {
                slidesToShow: 12,
                slidesToScroll: 12,
            }
        },
        {
            breakpoint: 1900,
            settings: {
                slidesToShow: 9,
                slidesToScroll: 9,
            }
        },
        {
            breakpoint: 1500,
            settings: {
                slidesToShow:8.8,
                slidesToScroll: 8.8,
            }
        },
        {
            breakpoint: 1410,
            settings: {
                slidesToShow: 7,
                slidesToScroll: 7,
            }
        },
        {
            breakpoint: 1250,
            settings: {
                slidesToShow: 6.3,
                slidesToScroll: 6.3,
            }
        },
        {
            breakpoint: 1030,
            settings: {
                slidesToShow: 6.65,
                slidesToScroll: 6.65,
            }
        },
        {
            breakpoint: 800,
            settings: {
                slidesToShow: 5,
                slidesToScroll: 5,
            }
        },
        {
            breakpoint: 600,
            settings: {
                slidesToShow: 3.3,
                slidesToScroll: 3.3,
            }
        },
        {
            breakpoint: 360,
            settings: {
                slidesToShow: 1.9,
                slidesToScroll: 1.9,
            }
        },      
    ]
})

const responsiveCategoryCarousel = document.querySelector('.js-carousel--responsive-category')

new Glider(responsiveCategoryCarousel, {
    slidesToShow: 2.68,
    slidesToScroll: 2.68,
    draggable: true,
    dots: '.js-carousel--responsive-category-dots' ,
    arrows: {
        prev: ".js-carousel--responsive-category-prev",
        next: ".js-carousel--responsive-category-next"
    },
    scrollLock: true,
    responsive: [
        {
            breakpoint: 2500,
            settings: {
                slidesToShow: 12,
                slidesToScroll: 12,
            }
        },
        {
            breakpoint: 1900,
            settings: {
                slidesToShow: 9,
                slidesToScroll: 9,
            }
        },
        {
            breakpoint: 1500,
            settings: {
                slidesToShow: 8.8,
                slidesToScroll: 8.8,
            }
        },
        {
            breakpoint: 1410,
            settings: {
                slidesToShow: 7,
                slidesToScroll: 7,
            }
        },
        {
            breakpoint: 1250,
            settings: {
                slidesToShow: 6.3,
                slidesToScroll: 6.3,
            }
        },
        {
            breakpoint: 1030,
            settings: {
                slidesToShow: 6.65,
                slidesToScroll: 6.65,
            }
        },
        {
            breakpoint: 800,
            settings: {
                slidesToShow: 5,
                slidesToScroll: 5,
            }
        },
        {
            breakpoint: 600,
            settings: {
                slidesToShow: 3.3,
                slidesToScroll: 3.3,
            }
        },
        {
            breakpoint: 360,
            settings: {
                slidesToShow: 1.9,
                slidesToScroll: 1.9,
            }
        },      
    ]
})






