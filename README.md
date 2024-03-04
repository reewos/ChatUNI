# ChatUNI
ChatUNI es un chatbot con arquitectura RAG, desarrollado para atender consultas respecto a las resoluciones rectorales de la UNI. 

## Desafío
En la mayoría de casos, la comunidad universitaria de la UNI no están enterados de muchas oportunidades como de becas, actividades académicas y administrativas o nuevos reglamentos que aparecen en la resoluciones rectorales de la universidad. Si bien es cierto, las resoluciones de la universidad están alojadas de manera pública, el problema es buscar exactamente una información de interés para el usuario dentro de todas las resoluciones publicadas.

## Desarrollo
Por tal razón, se ha construido un chatbot para atender estas consultas. De manera que, el usuario puede interactuar con el chatbot y obtener respuestas a sus consultas. Esto ayuda a la democratización de la información para todos, principalmente para la comunidad universitaria de la UNI.

Para el desarrollo del chatbot, se realizado los siguientes pasos:

### Web scraping de resoluciones rectorales de la UNI
La resoluciones rectorales de la UNI se encuentran en la siguiente página: [Resoluciones rectorales](https://portal.uni.edu.pe/index.php/encuentromultidiciplinario/2-uncategorised/230-resoluciones-rectorales-de-la-universidad-nacional-de-ingenieria) .

### Ingesta de datos para la base de datos vectorial
Se ha utilizado la base de datos vectorial de Pinecone para guardar las resoluciones rectorales.

### Creación del chatbot usando Gemini como LLM
Se ha utilizado Gemini como LLM para la creación del chatbot.

### Publicación en Streamlit
Se ha publicado el chatbot en Streamlit.


## Observaciones
Actualmente, este prototipo solo cuenta con las resoluciones del mes de enero de 2024. Aún se están realizando cambios en la estructura de la aplicación.

En algunas consultas, el chatbot no responde con la información solicitada, o responde con información parcial.


## Tecnologías usadas
- [Streamlit](https://streamlit.io/)
- [Pinecone](https://www.pinecone.io/)
- [HuggingFace](https://huggingface.co/)
- [Llama-index](https://docs.llamaindex.ai/en/stable/)
- [Gemini](https://gemini.google.com/)


## Referencias
- [ChatUNI - GitHub](https://github.com/reewos/ChatUNI)
- [Demo en Streamlit](https://chatuni.streamlit.app/)

## Autor
Reewos Talla 
- [https://github.com/reewos](https://github.com/reewos)
- [https://www.linkedin.com/in/reewos-talla-chumpitaz/](https://www.linkedin.com/in/reewos-talla-chumpitaz/)
