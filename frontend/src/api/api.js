import axios from 'axios'

export const api = axios.create({
    // baseURL: 'http://10.249.76.80:8000/api',
    baseURL: 'http://127.0.0.1:8000/api',
})