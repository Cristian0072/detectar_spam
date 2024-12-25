const URL = process.env.URL_API;
import axios from 'axios';

// Metodo POST
export const POST = async (recurso, data, token = "NONE") => {
    let headers = {
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    }
    if (token !== "NONE") {
        headers.headers["X-Access-Tokens"] = token;
    }
    console.log("URL: ", URL + recurso);
    return await axios.post(URL + recurso, data, headers);
}

// Metodo GET
export const GET = async (recurso, token = "NONE") => {
    let headers = {
        headers: {
            "Accept": "application/json",
        }
    }
    if (token !== "NONE") {
        headers.headers["X-Access-Tokens"] = token;
    }
    return await axios.get(URL + recurso, headers);
}