import axios from "axios"

const api = axios.create({
    baseURL: "https://stemstarserver-8.onrender.com/"
})

export default api