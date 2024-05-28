let pagina = 1; // comienza en la primera página

window.onscroll = function() {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
        // el usuario ha llegado al final de la página, carga más contenido
        cargarMasContenido();
    }
};

function cargarMasContenido() {
    pagina++; // incrementa el número de página
    fetch(`https://rickandmortyapi.com/api/character?page=${pagina}`)
        .then(response => response.json())
        .then(data => {
            // procesa los datos y agrega el contenido a tu página
            data.results.forEach(personaje => {
                let div = document.createElement('div');
                div.className = 'personaje';

                let img = document.createElement('img');
                img.src = personaje.image; // asumiendo que quieres mostrar la imagen del personaje
                div.appendChild(img);

                let container = document.createElement('div');
                container.className = 'container';

                let name = document.createElement('h4');
                name.textContent = personaje.name; // asumiendo que quieres mostrar el nombre del personaje
                container.appendChild(name);

                div.appendChild(container);

                document.getElementById('feed').appendChild(div);
            });
        });
}


