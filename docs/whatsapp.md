# Integracion WhatsApp (Cloud API)

Documento de referencia para implementar la integracion real con WhatsApp Business Platform (Cloud API).

## Requisito clave sobre el numero

- Se recomienda un numero **nuevo y dedicado** para pruebas y desarrollo.
- El numero **no puede tener WhatsApp activo**. Si esta registrado en WhatsApp personal, hay que desregistrarlo.

## Prerrequisitos

1) Cuenta de Meta Business verificada.
2) App en Meta Developers con producto **WhatsApp**.
3) WhatsApp Business Account (WABA) asociada.
4) Numero dedicado para registrar en WABA (sin WhatsApp activo).
5) Access Token (temporal para pruebas o de larga duracion para prod).
6) Webhook URL publica con HTTPS.
7) App Secret para validar firmas.

## Credenciales necesarias

- `ACCESS_TOKEN`: token para llamadas al Graph API.
- `PHONE_NUMBER_ID`: ID del numero en WhatsApp.
- `WABA_ID`: ID de la cuenta de WhatsApp Business.
- `APP_SECRET`: secreto de la app para firmas.
- `VERIFY_TOKEN`: token propio para validacion inicial del webhook.

## Opciones de pruebas

- **Sandbox de Meta**: numero de prueba provisto por Meta.
- **Numero propio**: para produccion o QA con control total.

## Plan de integracion (tecnico)

### Fase A - Configuracion Meta

- Crear app en https://developers.facebook.com/.
- Agregar producto WhatsApp.
- Asociar a WABA.
- Registrar numero y obtener `PHONE_NUMBER_ID`.
- Generar `ACCESS_TOKEN`.
- Definir `VERIFY_TOKEN`.

### Fase B - Webhook real

- Endpoint **GET** para verificacion:
  - Campos: `hub.mode`, `hub.verify_token`, `hub.challenge`.
- Validacion de firma:
  - Header: `X-Hub-Signature-256`.
  - HMAC SHA256 con `APP_SECRET` sobre el body.
- Parseo del payload oficial de WhatsApp:
  - Extraer texto del mensaje.
  - Manejar tipos (texto, voz, multimedia) en futuras fases.

### Fase C - Envio de mensajes

- POST al Graph API:
  - `https://graph.facebook.com/vXX.X/{PHONE_NUMBER_ID}/messages`
- Mensajes iniciales:
  - Bienvenida.
  - Prompt diario.
  - Feedback posterior a la respuesta.

### Fase D - Pruebas end-to-end

- Verificar recepcion de mensajes reales.
- Enviar respuesta automatica.
- Revisar logs y manejar errores del Graph API.

## Notas operativas

- El webhook debe ser publico y con HTTPS (ngrok o Cloudflare Tunnel).
- Guardar secretos en variables de entorno.
- No usar el numero personal para evitar interrupciones.
