import { POST } from "./conexion";

export const obtener_clasificacion_spam = async (data) => {
    try {
        //const token = Cookies.get('token');
        const response = await POST(`detectar_spam`, data);
        return response.data;
    } catch (error) {
        console.log("Error al obtener clasificación:", error);
        throw error;
    }
}