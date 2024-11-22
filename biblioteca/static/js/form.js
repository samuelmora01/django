document.addEventListener('DOMContentLoaded', function() {
    const showFormButton = document.getElementById('show-form');
    const modal = document.getElementById('modal');
    const formContainer = document.getElementById('form-container');
    const closeModalButton = modal.querySelector('.close-btn');
    const radioButtons = document.querySelectorAll('.radio');
    const typeRadio = document.querySelector('input[name="type"]');
    
    // Mostrar el modal cuando se hace clic en "Agregar libro"
    showFormButton.addEventListener('click', () => {
        modal.classList.add('active');
    });

    // Cerrar el modal cuando se hace clic en "Cerrar"
    closeModalButton.addEventListener('click', () => {
        modal.classList.remove('active');
        formContainer.innerHTML = '';  // Limpiar el contenido del formulario cuando se cierra
    });

    // Manejo de selección de tipo de libro (físico o digital)
    radioButtons.forEach((radio) => {
        radio.addEventListener('change', (event) => {
            const selectedType = event.target.value;
            loadForm(selectedType);  // Cargar el formulario según el tipo de libro
        });
    });

    // Función para cargar el formulario correspondiente según el tipo de libro
    function loadForm(type) {
        fetch(`/?type=${type}`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // Indica que es una solicitud AJAX
            },
        })
        .then((response) => response.text())
        .then((html) => {
            formContainer.innerHTML = html; // Insertar el formulario en el contenedor
            formContainer.querySelector('form').addEventListener('submit', (e) => {
                e.preventDefault();  // Prevenir el comportamiento por defecto del formulario
                handleFormSubmit(e.target, type);  // Manejar la acción de enviar el formulario
            });
        })
        .catch((error) => {
            console.error('Error al cargar el formulario:', error);
        });
    }

    // Función para manejar el envío del formulario
    function handleFormSubmit(form, type) {
        const formData = new FormData(form);
        const url = type === 'fisico' ? '/guardar_libro_fisico/' : '/guardar_libro_digital/';
        const method = form.method;

        // Realizar solicitud AJAX para guardar el libro
        fetch(url, {
            method: method,
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Libro guardado exitosamente.');
                form.reset();  // Limpiar el formulario después de guardar
                modal.classList.remove('active');  // Cerrar el modal
                formContainer.innerHTML = '';  // Limpiar el formulario cargado
            } else {
                alert('Error al guardar el libro.');
            }
        })
        .catch(error => {
            console.error('Error en la solicitud:', error);
            alert('Ocurrió un error al procesar la solicitud.');
        });
    }
});
