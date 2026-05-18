import axios from "axios"

const api = axios.create({
    baseURL: "stemstarserver-production.up.railway.app/"
})

export default api