def codeStructure():
    html = """
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="description" content="Astro description">
            <meta name="viewport" content="width=device-width">
            <link rel="icon" type="image/svg+xml" href="/favicon.svg">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">

            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css" integrity="sha512-z3gLpd7yknf1YoNbCzqRKc4qyor8gaKU1qmn+CShxbuBusANI9QpRohGBreCFkKxLhei6S9CQXFEbbKuqLg0DA==" crossorigin="anonymous" referrerpolicy="no-referrer">
            <title>Código de verificación</title>
	
		    <style>
                main {
                    min-width: 100%;
                }

                section {
                    margin: 0;
                    width: 100%;
                }

                .fl__header {
                    border-radius: 12px;
                    background: #38a3a2;
                    text-align: center;
                    margin: 2rem .75rem;
                    padding: .75rem 0;
                }

                .fl__header>h2 {
                    font-size: 2rem;
                    margin: 0;
                }

                *,
                body {
                    font-family: Poppins, sans-serif;
                    box-sizing: border-box;
                }

                h2,
                span,
                p {
                    color: #f8f8f8;
                }

                @media screen and (min-width: 640px) {

                    main {
                        min-width: 900px;
                        max-width: 900px;
                        margin: auto;
                        padding: 1rem;
                    }

                    .fl__header {
                        width: 480px;
                        margin: auto;
                    }

                    #code_box {
                        width: 250px;
                    }
                }
            </style>
	    </head>
	    <body>
		
            <main>
                <!-- HEADER -->
                <header>
                    <div class="fl__header">
                        <h2>Flippo
                        </h2>
                    </div>
                </header>

                <section>
                    <div style="width: 100%; padding: 1rem;">
                        <div style="width: 100%; text-align: center">
                            <h3 style="font-family: Poppins, sans-serif; font-size:28px; color: #181823">Autorizar Nuevo Dispositivo</h3>
                        </div>

                        <!-- CODE -->
                        <div style="width: 100%; padding: 1rem; margin-top: .5rem">
                            <div style="width: 100%">
                                <p style="color: #161616; font-family: Poppins, sans-serif; font-weight: 200; font-size: 14px; text-align: center">
                                    Si reconoce esta actividad, por favor confirmela con el siguiente código.</p>
                            </div>
                            <!-- CODIGO -->
                            <div id="code_box" style="background: #e0e0df; border-radius: 12px; padding: .5rem; margin: auto; text-align: center; margin-top: 1rem; letter-spacing: 8px">
                                <span style="color: #161616;font-family: Poppins, sans-serif; font-weight: bold; font-size: 1.5rem; line-height: 2rem">
                                    {{.Payload.code}}
                                </span>
                            </div>
                            <div style="width: 100%; margin-top: .5rem" class="w-full mt-2">
                                <p style="color: #161616; font-family: Poppins, sans-serif; font-weight: 200; font-size: 12px; text-align: center">
                                    Tenga en cuenta que este código solo es válido durante 15 minutos.
                                </p>
                            </div>
                        </div>

                        <!-- PROTETED ACCOUNT -->
                        <div style="width: 100%; padding: 1rem; margin-top: 1rem;">
                            <div style="margin-right:1rem;">
                                <i class="fa-solid fa-triangle-exclamation"></i>
                            </div>
                            <span style="color: #161616; font-family: Poppins, sans-serif; font-weight: bold; font-size: 1.5rem; margin-top: 1rem; margin-bottom: 1rem;">
                                ¿No eres tú?
                            </span>

                            <p style="color: #161616; font-family: Poppins, sans-serif; font-weight: 200; font-size: 14px; text-align: start">
                                Tomese unos minutos para asegurar su cuenta.
                            </p>

                            <div style="margin-top: 1rem;">
                                <button type="button" style="
                                border: none; outline: none; background: #38a3a2; border-radius: 24px; padding: .75rem 1.5rem;">
                                    <span style="color: #f8f8f8; font-family: Poppins, sans-serif; font-weight: bold; font-size: 1.25rem; text-align: center;">Protege tu cuenta</span>
                                </button>
                            </div>
                        </div>
                    </div>
                </section>
            </main>
	    </body>
    </html>
    """