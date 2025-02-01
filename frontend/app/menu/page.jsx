"use client";

import { useState, useCallback } from "react";
import debounce from "lodash/debounce";
import { obtener_clasificacion_spam } from "../hooks/servicio_spam";

export default function Menu() {
  const [texto, setTexto] = useState("");
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(null);
  const [info, setInfo] = useState(null);

  const enviar_texto = async (nuevo_texto) => {
    setError(null);
    setResultado(null);

    // Validación: texto vacío o menos de 10 palabras
    if (!nuevo_texto.trim() || nuevo_texto.split(" ").length < 10) {
      setInfo("Por favor, introduce un texto con al menos 10 palabras");
      setResultado(null);
      return;
    } else {
      setInfo(null);
    }

    try {
      // se convierte a JSON para enviarlo al backend
      const entrada = JSON.stringify({ texto: nuevo_texto.trim() });
      const respuesta = await obtener_clasificacion_spam(entrada);
      console.log(respuesta);
      if (respuesta && respuesta.resultado) {
        console.log("Resultado:", respuesta.resultado);
        setResultado(respuesta.resultado);
      } else {
        setResultado("No se pudo clasificar el mensaje.");
      }
    } catch (error) {
      console.log("Error al clasificar:", error);
      setResultado("Hubo un error. Intenta de nuevo.");
    }
  };
  // se crea una función que envía el texto con un retraso de 500ms
  const enviar_con_retraso = useCallback(
    debounce((nuevoTexto) => {
      enviar_texto(nuevoTexto);
    }, 1000),
    []
  );

  // función que maneja el cambio de texto
  const manejar_cambio_texto = (e) => {
    const nuevoTexto = e.target.value;
    setTexto(nuevoTexto);

    if (!nuevoTexto.trim()) {
      setInfo(null);
      setResultado(null);
    }
    enviar_con_retraso(nuevoTexto);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="text-2xl font-bold mb-4">Clasificador de mensajes SPAM</h1>
      <form className="w-full max-w-md flex flex-col">
        <textarea
          placeholder="Escriba el mensaje aquí..."
          value={texto}
          onChange={manejar_cambio_texto}
          className="border rounded p-2 mb-4 w-full h-60 text-black resize-none"
        />

      </form>
      {error && (
        <div className="mt-4 text-lg font-semibold text-center p-4 bg-red-100 text-red-700 rounded">
          Error: {error}
        </div>
      )}
      {info && (
        <div className="mt-4 text-lg font-semibold text-center p-4 bg-blue-100 text-blue-700 rounded">
          Información: {info}
        </div>
      )}
      {resultado !== null && !error && (
        <div className="mt-4 text-lg font-semibold text-center p-4 bg-black-500 rounded">
          Resultado: {resultado}
        </div>
      )}
    </div>
  );
}