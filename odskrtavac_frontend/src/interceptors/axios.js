import axios from 'axios';

axios.defaults.baseURL = "http://127.0.0.1:8000/";

let refresh = false;

axios.interceptors.response.use(resp => resp, async error => {
    if (error.response.status === 401 && !refresh) {
        refresh = true;

        const oldRefreshToken = localStorage.getItem('refresh_token');
        try {
            const { status, data } = await axios.post('user-api/refresh-token/', {
                refresh: oldRefreshToken
            }, {
                withCredentials: true
            });

            if (status === 200) {
                localStorage.setItem('access_token', data.access);
                axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`;

                if (data.refresh) {
                    localStorage.setItem('refresh_token', data.refresh);
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
