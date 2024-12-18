import axios from 'axios';

axios.defaults.baseURL = "https://odskrtavac-backend.onrender.com/";

let refresh = false;

axios.interceptors.response.use(resp => resp, async error => {
    if (error.response.status === 401 && !refresh) {
        refresh = true;

        const oldRefreshToken = localStorage.getItem('refreshToken');
        try {
            const { status, data } = await axios.post('user-api/refresh-token/', {
                refresh: oldRefreshToken
            }, {
                withCredentials: true
            });

            if (status === 200) {
                localStorage.setItem('accessToken', data.access);
                axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;

                if (data.refresh) {
                    localStorage.setItem('refreshToken', data.refresh);
                }

                error.config.headers['Authorization'] = `Bearer ${data.access}`;
                return axios(error.config);
            }
        } catch (refreshError) {
            console.error("Token refresh failed:", refreshError);
        }
    }
    refresh = false;
    return Promise.reject(error);
});
