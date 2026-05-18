import axios from "axios"

const api = axios.create({
    baseURL: "https://stemstarserver-81vf.onrender.com/"
})

export default api