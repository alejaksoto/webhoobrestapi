/**
 * Inicialización del SDK de Facebook para su uso en autenticación y eventos de la aplicación.
 */
window.fbAsyncInit = function () {
    FB.init({
        appId: '530977999838510', // ID de la aplicación configurada en Facebook Developer
        autoLogAppEvents: true, // Habilita el registro automático de eventos
        xfbml: true, // Procesa los plugins de Facebook declarados en la página
        version: 'v21.0' // Versión del SDK de Facebook
    });
    FB.AppEvents.logPageView(); // Registra la visualización de la página
};

// Session logging message event listener
window.addEventListener('message', function(event) {
    if (event.origin !== "https://www.facebook.com" && event.origin !== "https://web.facebook.com") return;
    try {
        var data = JSON.parse(event.data);
        if (data.type === 'WA_EMBEDDED_SIGNUP') {
          console.log('message event: ', data); // remove after testing
          
          // Determinar si el flujo fue exitoso o abandonado
        var endpoint = '/process-signup-event/'; // Ajusta este endpoint a la ruta de tu vista
        var payload = {
            event: data.event,
            type: data.type,
            data: data.data,
          };
      
          // Enviar datos al servidor
        fetch(endpoint, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCSRFToken(), // Incluye el CSRF token si es necesario
            },
            body: JSON.stringify(payload),
            })
            .then(function(response) {
              if (!response.ok) {
                console.error('Error al enviar los datos al servidor:', response.statusText);
              }
              return response.json();
            })
            .then(function(result) {
              console.log('Respuesta del servidor:', result);
            })
            .catch(function(error) {
              console.error('Error en la solicitud:', error);
            });
        }
        } catch (e) {
            console.log('message event: ', event.data); // remove after testing
      }
      
  });

/**
 * Carga asíncrona del SDK de Facebook mediante la creación de un script dinámico.
 * @param {Document} d - Referencia al documento HTML
 * @param {string} s - Tipo de elemento a crear ('script')
 * @param {string} id - ID único para el script cargado
 */
(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) { return; } // Verifica si el script ya está cargado
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js"; // URL del SDK de Facebook
    fjs.parentNode.insertBefore(js, fjs); // Inserta el script antes del primer script existente
}(document, 'script', 'facebook-jssdk'));

/**
 * Verifica el estado de inicio de sesión de Facebook al cargar la página.
 */
window.onload = function () {
    FB.getLoginStatus(function (response) {
        statusChangeCallback(response); // Maneja la respuesta del estado de inicio de sesión
    });
};

/**
 * Maneja los cambios en el estado de autenticación del usuario.
 * @param {Object} response - Objeto de respuesta del estado de inicio de sesión
 */
function statusChangeCallback(response) {
    console.log('Login status:', response);
    if (response.status === 'connected') {
        var userID = response.authResponse.userID;
        var accessToken = response.authResponse.accessToken;

        console.log('Usuario conectado con ID:', userID);
        console.log('Access Token:', accessToken);
        window.location.href = '/app-logged-in'; // Redirige al usuario a la aplicación autenticada
    } else if (response.status === 'not_authorized') {
        console.log('Usuario no autorizado en la app.');
        showLoginButton(); // Muestra el botón de inicio de sesión
    } else {
        console.log('Usuario no conectado.');
        showLoginButton(); // Muestra el botón de inicio de sesión
    }
}

/**
 * Muestra el botón de inicio de sesión en la interfaz de usuario.
 */
function showLoginButton() {
    document.getElementById('loginButton').style.display = 'block'; // Despliega el botón de inicio de sesión
}

/**
 * Lanza el registro embebido para WhatsApp Business mediante el SDK de Facebook.
 */
window.launchWhatsAppSignup = function() {
    FB.login(fbLoginCallback, {
        config_id: '4004802773140221', // Configuración de la app de WhatsApp Business
        response_type: 'code', // Tipo de respuesta esperado
        override_default_response_type: true, // Fuerza el tipo de respuesta definido
        extras: {
            setup: {},
            featureType: '',
            sessionInfoVersion: '3', // Versión de información de sesión
        }
    });
};



/**
 * Callback para manejar la respuesta del inicio de sesión en Facebook.
 * @param {Object} response - Objeto de respuesta de autenticación
 */
function fbLoginCallback(response) {
    var errorElement = document.getElementById('error-message');
    if (errorElement) {
        errorElement.style.display = 'none';
    }

    // Validar la respuesta inicial
    if (!response || !response.authResponse || !response.authResponse.accessToken) {
        handleLoginError(new Error('Token de autenticación no encontrado'));
        return;
    }

    var accessToken = response.authResponse.accessToken;

    // Enviar access token al backend
    fetch('/process_token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
            'Accept': 'application/json'
        },
        credentials: 'same-origin',
        body: JSON.stringify({ 
            code: accessToken,
            userId: response.authResponse.userID || ''
        })
    })
    .then(function(res) {
        if (!res.ok) {
            return res.text().then(function(errorText) {
                throw new Error('Error del servidor (' + res.status + '): ' + errorText);
            });
        }
        return res.json();
    })
    .then(function(data) {
        if (!data.success) {
            throw new Error(data.message || 'Error en la autenticación');
        }
        // Redirigir en caso de éxito
        window.location.href = data.redirect || '/dashboard';
    })
    .catch(function(error) {
        handleLoginError(error);
    });

    function handleLoginError(error) {
        console.error('Error en el proceso de login:', error);

        // Mostrar botón de login
        showLoginButton();

        // Mostrar mensaje de error
        if (errorElement) {
            errorElement.textContent = error.message || 'Error en el inicio de sesión. Por favor, intenta nuevamente.';
            errorElement.style.display = 'block';
        }

        // Si hay un callback de error definido, llamarlo
        if (typeof onLoginError === 'function') {
            onLoginError(error);
        }
    }
}
