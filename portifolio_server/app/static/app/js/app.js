// const sections = document.querySelectorAll('section');
// sections.forEach(section => {
//   section.classList.add('hidden');
// });



const observer = new IntersectionObserver((entries)=> {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
        } else {
        }

    });
},{ threshold: 0 });




const hiddenElements = document.querySelectorAll('.hidden');
hiddenElements.forEach((el) => observer.observe(el));