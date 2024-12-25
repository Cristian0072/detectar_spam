"use client";

import { useState } from "react";
import { obtener_clasificacion_spam } from "../hooks/servicio_spam";

export default function Home() {
  const [texto, setTexto] = useState("");
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(null);

  const enviar = async () => {
    setError(null);
    // se asegura que el texto no esté vacío
    if (!texto.trim()) {
      setError("Por favor, introduce un texto para clasificar");
      return;
    }

    try {

      // se convierte a JSON para enviarlo al backend
      const entrada = JSON.stringify({ texto: String(texto).trim() });
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

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <h1 className="text-2xl font-bold mb-4">Clasificador de mensajes SPAM</h1>
      <form onSubmit={enviar} className="w-full max-w-md flex flex-col">
        <textarea
          placeholder="Escriba el mensaje aquí..."
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          className="border rounded p-2 mb-4 w-full h-32 text-black resize-none"
        />
        <button
          type="button"
          onClick={enviar}
          className="bg-green-700 text-white py-2 px-4 rounded hover:bg-green-600 font-bold transition-colors"
        >
          Clasificar
        </button>
      </form>
      {error && (
        <div className="mt-4 text-lg font-semibold text-center p-4 bg-red-100 text-red-700 rounded">
          {error}
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